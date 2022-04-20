"""Stream type classes for tap-hubspot."""
# from black import Report
import requests
import singer
import json

from dateutil import parser
import datetime

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


class CallsStream(HubspotStream):
    # _LOG_REQUEST_METRICS_URL=True
    name = "calls"
    path = f"/crm/v3/objects/{name}/search"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"
    rest_method = "POST"
    extra_params = []
    filter = {}
    date = "2015-08-21T00:30:09.408Z"


    @property
    def schema(self) -> dict:
        """Return the schema for this stream."""
        schema, self.extra_params = self.get_custom_schema(poorly_cast=[])
        return schema

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        self.filter = self.custom_hubspot_filter_request(response)
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def custom_hubspot_filter_request(self, response: requests.Response) -> dict:
        """Return the filter for the request."""
        org_date = self.date
        value = parser.parse(org_date)
        highvalue = value + datetime.timedelta(days=30)

        filter = {
            "propertyName": "hs_lastmodifieddate",
            "operator": "BETWEEN",
            "value": str(int(value.timestamp())*1000),
            "highValue": str(int(highvalue.timestamp())*1000)
        }

        return filter

    # Loop condition
    def get_next_page_token(self, response: requests.Response, previous_token: Optional[Any]) -> Optional[Any]:
        """Return the next page token from the response."""
        token = super().get_next_page_token(response, previous_token)
        # if parser.parse(self.date) + datetime.timedelta(days=30) > datetime.date.today():
            # return None
        if token is None:
            if parser.parse(self.date) + datetime.timedelta(days=30) > datetime.date.today():
                return None
            token = 0
        return token

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.
        """

        ret = {
            "properties": self.extra_params,
            "limit": 100,
            "after": next_page_token,
            "sorts": [
                {
                    "propertyName": "hs_lastmodifieddate",
                    "direction": "ASCENDING"
                }
            ]
        }
        if self.filter:
            ret["filterGroups"] =[{
                "filters": [self.filter]
            }]
        print(ret)
        return ret
class CompaniesStream(HubspotStream):
    name = "companies"
    path = f"/crm/v3/objects/{name}/search"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"
    rest_method = "POST"
    extra_params = []

    @property
    def schema(self) -> dict:
        """Return the schema for this stream."""
        schema, self.extra_params = self.get_custom_schema(poorly_cast=[])
        return schema



    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.
        """
        return {
            "properties": self.extra_params,
            "limit": 100,
            "after": next_page_token,
        }

class ContactsStream(HubspotStream):
    name = "contacts"
    path = f"/crm/v3/objects/{name}/search"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"
    rest_method = "POST"
    extra_params = []

    @property
    def schema(self) -> dict:
        """Return the schema for this stream."""
        schema, self.extra_params = self.get_custom_schema(poorly_cast=[])
        return schema

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.
        """
        return {
            "properties": self.extra_params,
            "limit": 100,
            "after": next_page_token,
        }



class DealsStream(HubspotStream):
    name = "deals"
    path = f"/crm/v3/objects/{name}/search"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"
    rest_method = "POST"
    extra_params = []

    @property
    def schema(self) -> dict:
        """Return the schema for this stream."""
        schema, self.extra_params = self.get_custom_schema(poorly_cast=[])
        return schema

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.
        """
        return {
            "properties": self.extra_params,
            "limit": 100,
            "after": next_page_token,
        }

class DealPipelineStream(HubspotStream):
    name = "deal_pipelines"
    path = "/crm/v3/pipelines/deals"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"
    schema_filepath = SCHEMAS_DIR / f"{name}.json"


# TODO Remove engagements once acceptable
class EngagementsStream(HubspotStream):
    name = "engagements"
    path = "/engagements/v1/engagements/paged"
    primary_keys = ["id"]
    replication_key = "lastUpdated"
    records_jsonpath = "$.results.[*]"
    next_page_token_jsonpath = "$.offset"
    schema_filepath = SCHEMAS_DIR / f"{name}.json"

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


class EmailsStream(HubspotStream):
    name = "emails"
    path = f"/crm/v3/objects/{name}/search"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"
    rest_method = "POST"
    extra_params = []

    @property
    def schema(self) -> dict:
        """Return the schema for this stream."""
        schema, self.extra_params = self.get_custom_schema(poorly_cast=[])
        return schema

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.
        """
        return {
            "properties": self.extra_params,
            "limit": 100,
            "after": next_page_token,
        }

# class FormsStream(HubspotStream):
#     name = "forms"
#     path = "/forms/v2/forms"
#     primary_keys = ["id"]
#     replication_key = "updatedAt"
#     records_jsonpath = "$.results[*]"
#     next_page_token_jsonpath = "$.paging.next.after"

class MeetingsStream(HubspotStream):
    name = "meetings"
    path = f"/crm/v3/objects/{name}/search"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"
    rest_method = "POST"
    extra_params = []

    @property
    def schema(self) -> dict:
        """Return the schema for this stream."""
        schema, self.extra_params = self.get_custom_schema(poorly_cast=[])
        return schema

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.
        """
        return {
            "properties": self.extra_params,
            "limit": 100,
            "after": next_page_token,
        }

class NotesStream(HubspotStream):
    name = "notes"
    path = f"/crm/v3/objects/{name}/search"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"
    rest_method = "POST"
    extra_params = []

    @property
    def schema(self) -> dict:
        """Return the schema for this stream."""
        schema, self.extra_params = self.get_custom_schema(poorly_cast=[])
        return schema

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.
        """
        return {
            "properties": self.extra_params,
            "limit": 100,
            "after": next_page_token,
        }
class OwnersStream(HubspotStream):
    """Define custom stream."""
    name = "owners"
    path = "/crm/v3/owners"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"
    schema_filepath = SCHEMAS_DIR / f"{name}.json"

class TasksStream(HubspotStream):
    name = "tasks"
    path = f"/crm/v3/objects/{name}/search"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.after"
    rest_method = "POST"
    extra_params = []

    @property
    def schema(self) -> dict:
        """Return the schema for this stream."""
        schema, self.extra_params = self.get_custom_schema(poorly_cast=[])
        return schema

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.
        """
        return {
            "properties": self.extra_params,
            "limit": 100,
            "after": next_page_token,
        }

class WorkflowsStream(HubspotStream):
    name = "workflows"
    path = "/automation/v3/workflows"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.workflows[*]"
    schema_filepath = SCHEMAS_DIR / f"{name}.json"









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





