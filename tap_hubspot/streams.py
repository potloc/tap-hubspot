"""Stream type classes for tap-hubspot."""
# from black import Report
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union

import pytz
import requests
from tap_hubspot.client import HUBSPOT_OBJECTS, HubspotStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

utc = pytz.UTC


class MeetingsStream(HubspotStream):
    name = "meetings"
    path = "/crm/v3/objects/meetings"
    primary_keys = ["id"]

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        selected_properties = self.get_selected_properties()
        params = super().get_url_params(context, next_page_token)
        params["properties"] = ",".join(selected_properties)
        return params

    @property
    def schema(self) -> dict:
        if self.cached_schema is None:
            self.cached_schema, self.properties = self.get_custom_schema()
        return self.cached_schema


class CallsStream(HubspotStream):
    name = "calls"
    path = "/crm/v3/objects/calls"
    primary_keys = ["id"]

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        selected_properties = self.get_selected_properties()
        params = super().get_url_params(context, next_page_token)
        params["properties"] = ",".join(selected_properties)
        return params

    @property
    def schema(self) -> dict:
        if self.cached_schema is None:
            self.cached_schema, self.properties = self.get_custom_schema()
        return self.cached_schema


class OwnersStream(HubspotStream):
    """Define custom stream."""
    name = "owners"
    path = "/crm/v3/owners"
    primary_keys = ["id"]
    partitions = [{"archived": True}, {"archived": False}]

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params["archived"] = context["archived"]
        return params


class CompaniesStream(HubspotStream):
    """Define custom stream."""

    name = "companies"
    path = "/crm/v3/objects/companies"
    primary_keys = ["id"]
    partitions = [{"archived": True}, {"archived": False}]


    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        selected_properties = self.get_selected_properties()
        params = super().get_url_params(context, next_page_token)
        params["properties"] = ",".join(selected_properties)
        params["archived"] = context["archived"]
        params["associations"] = ",".join(HUBSPOT_OBJECTS)
        return params

    @property
    def schema(self) -> dict:
        if self.cached_schema is None:
            self.cached_schema, self.properties = self.get_custom_schema()
        return self.cached_schema

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {"archived": record["archived"], "company_id": record["id"]}


class DealsStream(HubspotStream):
    """Define custom stream."""
    name = "deals"
    path = "/crm/v3/objects/deals"
    primary_keys = ["id"]
    partitions = [{"archived": True}, {"archived": False}]

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        selected_properties = self.get_selected_properties()
        params = super().get_url_params(context, next_page_token)
        params["properties"] = ",".join(selected_properties)
        params["archived"] = context["archived"]
        params["associations"] = ",".join(HUBSPOT_OBJECTS)
        return params

    @property
    def schema(self) -> dict:
        if self.cached_schema is None:
            self.cached_schema, self.properties = self.get_custom_schema()
        return self.cached_schema

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "archived": record["archived"],
            "deal_id": record["id"],
        }


class ContactsStream(HubspotStream):
    """Define custom stream."""

    name = "contacts"
    path = "/crm/v3/objects/contacts"
    primary_keys = ["id"]
    partitions = [{"archived": True}, {"archived": False}]

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        selected_properties = self.get_selected_properties()
        params = super().get_url_params(context, next_page_token)
        params["properties"] = ",".join(selected_properties)
        params["archived"] = context["archived"]
        params["associations"] = ",".join(HUBSPOT_OBJECTS)
        return params

    @property
    def schema(self) -> dict:
        if self.cached_schema is None:
            self.cached_schema, self.properties = self.get_custom_schema()
        return self.cached_schema

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {"archived": record["archived"], "contact_id": record["id"]}


class PropertiesStream(HubspotStream):
    """Define custom stream."""

    schema_filepath = SCHEMAS_DIR / "properties.json"
    primary_keys = ["name"]

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        data = response.json()["results"]
        return [x for x in data if self.replication_key in x]


class PropertiesDealsStream(PropertiesStream):
    name = "properties_deals"
    path = "/crm/v3/properties/deals"


class PropertiesMeetingsStream(PropertiesStream):
    name = "properties_meetings"
    path = "/crm/v3/properties/meetings"


class PropertiesCompaniesStream(PropertiesStream):
    name = "properties_companies"
    path = "/crm/v3/properties/companies"


class PropertiesContactsStream(PropertiesStream):
    name = "properties_contacts"
    path = "/crm/v3/properties/contacts"


class AssociationsDealsToCompaniesStream(HubspotStream):
    name = "associations_deals_companies"
    path = "/crm/v4/objects/deals/{deal_id}/associations/companies"
    deal_id = ""
    replication_method = "FULL_TABLE"
    primary_keys = ["id", "toObjectId"]
    state_partitioning_keys = ["id"]
    replication_key = ""
    parent_stream_type = DealsStream
    schema_filepath = SCHEMAS_DIR / "associations_all.json"

    ignore_parent_replication_keys = True

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = super().get_url_params(context, next_page_token)
        self.deal_id = context["deal_id"]
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        data = response.json()["results"]
        ret = []
        for e in data:
            elem = e
            elem["id"] = self.deal_id
            ret.append(elem)

        return ret


class AssociationsDealsToContactsStream(HubspotStream):
    name = "associations_deals_contacts"
    path = "/crm/v4/objects/deals/{deal_id}/associations/contacts"
    deal_id = ""
    replication_method = "FULL_TABLE"
    primary_keys = ["id", "toObjectId"]
    state_partitioning_keys = ["id"]
    replication_key = ""
    parent_stream_type = DealsStream
    schema_filepath = SCHEMAS_DIR / "associations_all.json"

    ignore_parent_replication_keys = True

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = super().get_url_params(context, next_page_token)
        self.deal_id = context["deal_id"]
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        data = response.json()["results"]
        ret = []
        for e in data:
            elem = e
            elem["id"] = self.deal_id
            ret.append(elem)

        return ret


class AssociationsContactsToDealsStream(HubspotStream):
    name = "associations_contacts_deals"
    path = "/crm/v4/objects/contacts/{contact_id}/associations/deals"
    deal_id = ""
    replication_method = "FULL_TABLE"
    primary_keys = ["id", "toObjectId"]
    state_partitioning_keys = ["id"]
    replication_key = ""
    parent_stream_type = ContactsStream
    schema_filepath = SCHEMAS_DIR / "associations_all.json"

    ignore_parent_replication_keys = True

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = super().get_url_params(context, next_page_token)
        self.contact_id = context["contact_id"]
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        data = response.json()["results"]
        ret = []
        for e in data:
            elem = e
            elem["id"] = self.contact_id
            ret.append(elem)

        return ret


class AssociationsContactsToCompaniesStream(HubspotStream):
    name = "associations_contacts_companies"
    path = "/crm/v4/objects/contacts/{contact_id}/associations/companies"
    deal_id = ""
    replication_method = "FULL_TABLE"
    primary_keys = ["id", "toObjectId"]
    state_partitioning_keys = ["id"]
    replication_key = ""
    parent_stream_type = ContactsStream
    schema_filepath = SCHEMAS_DIR / "associations_all.json"

    ignore_parent_replication_keys = True

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = super().get_url_params(context, next_page_token)
        self.contact_id = context["contact_id"]
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        data = response.json()["results"]
        ret = []
        for e in data:
            elem = e
            elem["id"] = self.contact_id
            ret.append(elem)

        return ret


class AssociationsCompaniesToContactsStream(HubspotStream):
    name = "associations_companies_contacts"
    path = "/crm/v4/objects/companies/{company_id}/associations/contacts"
    deal_id = ""
    replication_method = "FULL_TABLE"
    primary_keys = ["id", "toObjectId"]
    state_partitioning_keys = ["id"]
    replication_key = ""
    parent_stream_type = CompaniesStream
    schema_filepath = SCHEMAS_DIR / "associations_all.json"

    ignore_parent_replication_keys = True

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = super().get_url_params(context, next_page_token)
        self.company_id = context["company_id"]
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        data = response.json()["results"]
        ret = []
        for e in data:
            elem = e
            elem["id"] = self.company_id
            ret.append(elem)

        return ret


class AssociationsCompaniesToDealsStream(HubspotStream):
    name = "associations_companies_deals"
    path = "/crm/v4/objects/companies/{company_id}/associations/deals"
    deal_id = ""
    replication_method = "FULL_TABLE"
    primary_keys = ["id", "toObjectId"]
    state_partitioning_keys = ["id"]
    replication_key = ""
    parent_stream_type = CompaniesStream
    schema_filepath = SCHEMAS_DIR / "associations_all.json"

    ignore_parent_replication_keys = True

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = super().get_url_params(context, next_page_token)
        self.company_id = context["company_id"]
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        data = response.json()["results"]
        ret = []
        for e in data:
            elem = e
            elem["id"] = self.company_id
            ret.append(elem)

        return ret


class QuotesStream(HubspotStream):
    name = "quotes"
    path = "/crm/v3/objects/quotes"
    primary_keys = ["id"]
    partitions = [{"archived": True}, {"archived": False}]

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        selected_properties = self.get_selected_properties()
        params = super().get_url_params(context, next_page_token)
        params["properties"] = ",".join(selected_properties)
        params["archived"] = context["archived"]
        params["associations"] = ",".join(HUBSPOT_OBJECTS)
        return params

    @property
    def schema(self) -> dict:
        if self.cached_schema is None:
            self.cached_schema, self.properties = self.get_custom_schema()
        return self.cached_schema

class LineItemsStream(HubspotStream):
    name = "line_items"
    path = "/crm/v3/objects/line_items"
    primary_keys = ["id"]
    partitions = [{"archived": True}, {"archived": False}]

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        selected_properties = self.get_selected_properties()
        params = super().get_url_params(context, next_page_token)
        params["properties"] = ",".join(selected_properties)
        params["archived"] = context["archived"]
        params["associations"] = ",".join(HUBSPOT_OBJECTS)
        return params

    @property
    def schema(self) -> dict:
        if self.cached_schema is None:
            self.cached_schema, self.properties = self.get_custom_schema()
        return self.cached_schema
