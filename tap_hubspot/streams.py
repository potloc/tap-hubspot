"""Stream type classes for tap-hubspot."""
import requests
import singer

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
class OwnersStream(HubspotStream):
    """Define custom stream."""
    name = "owners"
    path = "/crm/v3/owners"
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

class CompaniesStream(HubspotStream):
    name = "companies"
    path = "/crm/v3/objects/companies"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"

class DealPipelineStream(HubspotStream):
    name = "deal_pipelines"
    path = "/crm/v3/pipelines/deals"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"

class DealsStream(HubspotStream):
    name = "deals"
    path = "/crm/v3/objects/deals"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"


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





