"""Stream type classes for tap-hubspot."""
# from black import Report
from math import inf
import requests
import singer
import json

from dateutil import parser
import datetime, pytz
import time
from datetime import datetime

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
from tap_hubspot.streams import ContactsStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

LOGGER = singer.get_logger()
utc=pytz.UTC

from tap_hubspot.schemas.analytics import (
    AnalyticsViews,
)
class AnalyticsStream(HubspotStream):
    records_jsonpath = "$.[*]"  # Or override `parse_response`.
    schema_filepath = ""

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure.
        Returns row, or None if row is to be excluded"""

        if self.replication_key:
            if row[self.replication_key] <= self.get_starting_timestamp(context).astimezone(pytz.utc):
                return None
        return row

class AnalyticsViewsStream(AnalyticsStream):
    name = "analytics_views_v2"
    path = "/analytics/v2/views"
    primary_keys = ["id"]
    schema = AnalyticsViews.schema
    replication_key = "updatedDate"

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        data = response.json()
        ret = []
        for d in data:
            val = d
            val["updatedDate"] = datetime.strptime(d["updatedDate"], "%Y-%m-%d").astimezone(pytz.utc)
            ret.append(val)
        data = ret
        yield from extract_jsonpath(self.records_jsonpath, input=data)


