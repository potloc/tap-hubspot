"""Stream type classes for tap-hubspot."""
# from black import Report
import requests
import singer
import json

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk import typing as th  # JSON schema typing helpers
from tap_hubspot.client import PROPERTIES_DIR, HubspotStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

LOGGER = singer.get_logger()
class CompaniesStream(HubspotStream):
    name = "companies"
    path = "/crm/v3/objects/companies"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"
    extra_params = []

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = super().get_url_params(context, next_page_token)
        params['limit'] = 100

        return params
    @property
    def schema(self) -> dict:
        """Dynamically detect the json schema for the stream.
        This is evaluated prior to any records being retrieved.
        """
        internal_properties: List[th.Property] = []
        properties: List[th.Property] = []
        fuck_this = ['hs_object_id']

        properties_file_path = PROPERTIES_DIR / f"{self.name}.json"
        f = properties_file_path.open()
        properties_hub = json.load(f)['results']

        for prop in properties_hub:
            name = prop['name']
            self.extra_params.append(name)
            type = self.get_json_schema(prop['type'])
            if name in fuck_this:
                internal_properties.append(th.Property(name, th.StringType()))
            else:
                internal_properties.append(th.Property(name, type))

        properties.append(th.Property('updatedAt', th.StringType()))
        properties.append(th.Property('createdAt', th.StringType()))
        properties.append(th.Property('id', th.StringType()))
        properties.append(th.Property(
                'properties', th.ObjectType(*internal_properties)
            ))
        return th.PropertiesList(*properties).to_dict()

class ContactsStream(HubspotStream):
    name = "contacts"
    path = "/crm/v3/objects/contacts"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"
    extra_params = []

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = super().get_url_params(context, next_page_token)
        params['limit'] = 100

        return params
    @property
    def schema(self) -> dict:
        """Dynamically detect the json schema for the stream.
        This is evaluated prior to any records being retrieved.
        """
        internal_properties: List[th.Property] = []
        properties: List[th.Property] = []
        fuck_this = []

        properties_file_path = PROPERTIES_DIR / f"{self.name}.json"
        f = properties_file_path.open()
        properties_hub = json.load(f)['results']

        for prop in properties_hub:
            name = prop['name']
            self.extra_params.append(name)
            type = self.get_json_schema(prop['type'])
            if name in fuck_this:
                internal_properties.append(th.Property(name, th.StringType()))
            else:
                internal_properties.append(th.Property(name, type))

        properties.append(th.Property('updatedAt', th.StringType()))
        properties.append(th.Property('createdAt', th.StringType()))
        properties.append(th.Property('id', th.StringType()))
        properties.append(th.Property(
                'properties', th.ObjectType(*internal_properties)
            ))
        return th.PropertiesList(*properties).to_dict()

class DealsStream(HubspotStream):
    name = "deals"
    path = "/crm/v3/objects/deals"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"

    @property
    def schema(self) -> dict:
        """Dynamically detect the json schema for the stream.
        This is evaluated prior to any records being retrieved.
        """
        internal_properties: List[th.Property] = []
        properties: List[th.Property] = []

        properties_hub = requests.get(self.url_base+f"/crm/v3/properties/{self.name}", headers=self.http_headers).json()['results']
        for prop in properties_hub:
            name = prop['name']
            type = self.get_json_schema(prop['type'])
            internal_properties.append(th.Property(name, type))

        properties.append(th.Property('updatedAt', th.StringType()))
        properties.append(th.Property('createdAt', th.StringType()))
        properties.append(th.Property('id', th.StringType()))
        properties.append(th.Property(
                'properties', th.ObjectType(*internal_properties)
            ))
        return th.PropertiesList(*properties).to_dict()
class DealPipelineStream(HubspotStream):
    name = "deal_pipelines"
    path = "/crm/v3/pipelines/deals"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"

class EngagementsStream(HubspotStream):
    name = "engagements"
    path = "/engagements/v1/engagements/paged"
    primary_keys = ["id"]
    replication_key = "lastUpdated"
    records_jsonpath = "$.results.[*]"
    next_page_token_jsonpath = "$.offset"

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = super().get_url_params(context, next_page_token)
        if next_page_token:
            params["offset"] = next_page_token

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        response.raise_for_status()
        input = response.json()

        for elem in input["results"]:
            elem["id"] = elem["engagement"]["id"]
            elem["lastUpdated"] = elem["engagement"]["lastUpdated"]
        yield from extract_jsonpath(self.records_jsonpath, input=input)




class FormsStream(HubspotStream):
    name = "forms"
    path = "/forms/v2/forms"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"

class MeetingsStream(HubspotStream):
    name = "meetings"
    path = "/crm/v3/objects/meetings"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"
class OwnersStream(HubspotStream):
    """Define custom stream."""
    name = "owners"
    path = "/crm/v3/owners"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"

class WorkflowsStream(HubspotStream):
    name = "workflows"
    path = "/automation/v3/workflows"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.workflows[*]"









    # @property
    # def schema(self) -> dict:
    #     """Dynamically detect the json schema for the stream.
    #     This is evaluated prior to any records being retrieved.
    #     """
    #     internal_properties: List[th.Property] = []
    #     properties: List[th.Property] = []

    #     properties_hub = requests.get(self.url_base+f"/crm/v3/properties/{self.name}", headers=self.http_headers).json()['results']
    #     for prop in properties_hub:
    #         name = prop['name']
    #         type = self.get_json_schema(prop['type'])
    #         internal_properties.append(th.Property(name, type))

    #     properties.append(th.Property('updatedAt', th.StringType()))
    #     properties.append(th.Property('createdAt', th.StringType()))
    #     properties.append(th.Property('id', th.StringType()))
    #     properties.append(th.Property(
    #             'properties', th.ObjectType(*internal_properties)
    #         ))
    #     return th.PropertiesList(*properties).to_dict()





