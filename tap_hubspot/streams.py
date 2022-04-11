"""Stream type classes for tap-hubspot."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_hubspot.client import HubspotStream
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class OwnersStream(HubspotStream):
    """Define custom stream."""
    name = "owners"
    path = "/crm/v3/owners"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    records_jsonpath = "$.results[*]"
    next_page_token_jsonpath = "$.paging.next.link"
    # Optionally, you may also use `schema_filepath` in place of `schema`:





