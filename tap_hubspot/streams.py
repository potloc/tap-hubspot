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
    replication_key = "updatedAt"
    cached_schema = None
    properties = []

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
    replication_key = "updatedAt"

class CompaniesStream(HubspotStream):
    """Define custom stream."""
    name = "companies"
    path = "/crm/v3/objects/companies"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    cached_schema = None
    properties = []

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
    replication_key = "updatedAt"
    cached_schema = None
    properties = []

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
    name = ""
    path = f"/crm/v3/properties/{name}"
    primary_keys = ["name"]
    replication_key = "updatedAt"
    schema = th.PropertiesList(
                th.Property('updatedAt', th.DateTimeType, required=True),
                th.Property('createdAt', th.StringType, required=True),
                th.Property('name', th.StringType, required=True),
                th.Property('label', th.StringType, required=False),
                th.Property('type', th.StringType, required=False),
                th.Property('fieldType', th.StringType, required=False),
                th.Property('description', th.StringType, required=False),
                th.Property('groupName', th.StringType, required=False),
                th.Property('options',
                    th.ArrayType(
                        th.ObjectType(
                            th.Property('label', th.StringType, required=False),
                            th.Property('value', th.StringType, required=False),
                            th.Property('displayOrder', th.IntegerType, required=False),
                            th.Property('hidden', th.BooleanType, required=False),
                        )
                    ), required=False),
                th.Property('displayOrder', th.IntegerType, required=False),
                th.Property('calculated', th.BooleanType, required=False),
                th.Property('externalOptions', th.BooleanType, required=False),

                th.Property('hasUniqueValue', th.BooleanType, required=False),
                th.Property('hasUniqueValue', th.BooleanType, required=False),
                th.Property('hidden', th.BooleanType, required=False),
                th.Property('hubspotDefined', th.BooleanType, required=False),
                th.Property('modificationMetadata',
                    th.ObjectType(
                        th.Property('archivable', th.BooleanType, required=False),
                        th.Property('readOnlyDefinition', th.BooleanType, required=False),
                        th.Property('readOnlyOptions', th.BooleanType, required=False),
                        th.Property('readOnlyValue', th.BooleanType, required=False),
                    ), required=False),
                th.Property('formField', th.BooleanType, required=False),
            )

class PropertiesDealsStream(PropertiesStream):
    name = "deals"

class PropertiesMeetingsStream(PropertiesStream):
    name = "meetings"

class PropertiesCompaniesStream(PropertiesStream):
    name = "companies"








