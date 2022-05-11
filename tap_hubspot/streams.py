"""Stream type classes for tap-hubspot."""
# from black import Report
import requests
import singer
import json

from dateutil import parser
import datetime, pytz

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
from tap_hubspot.client import HubspotStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

LOGGER = singer.get_logger()
utc=pytz.UTC




class MeetingsStream(HubspotStream):
    name = "meetings"
    path = f"/crm/v3/objects/meetings"
    primary_keys = ["id"]

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params['properties'] = ','.join(self.properties)
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

class CompaniesStream(HubspotStream):
    """Define custom stream."""
    name = "companies"
    path = "/crm/v3/objects/companies"
    primary_keys = ["id"]

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params['properties'] = ','.join(self.properties)
        return params

    @property
    def schema(self) -> dict:
        if self.cached_schema is None:
            self.cached_schema, self.properties = self.get_custom_schema()
        return self.cached_schema

class DealsStream(HubspotStream):
    """Define custom stream."""
    name = "deals"
    path = "/crm/v3/objects/deals"
    primary_keys = ["id"]

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params['properties'] = ','.join(self.properties)
        return params

    @property
    def schema(self) -> dict:
        if self.cached_schema is None:
            self.cached_schema, self.properties = self.get_custom_schema()
        return self.cached_schema
class ContactsStream(HubspotStream):
    """Define custom stream."""
    name = "contacts"
    path = "/crm/v3/objects/contacts"
    primary_keys = ["id"]

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params['properties'] = ','.join(self.properties)
        return params

    @property
    def schema(self) -> dict:
        if self.cached_schema is None:
            self.cached_schema, self.properties = self.get_custom_schema()
        return self.cached_schema

class PropertiesStream(HubspotStream):
    """Define custom stream."""
    schema_filepath = SCHEMAS_DIR / "properties.json"
    primary_keys = ["name"]

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        data = response.json()['results']
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


class AssociationsStream(HubspotStream):
    name="associations_deals_companies"
    path = "/crm/v4/objects/deals/{id}/associations/companies"

    parent_stream_type = DealsStream

    ignore_parent_replication_keys = True







