"""Hubspot tap class."""

from typing import List
# from black import main

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
from tap_hubspot.streams import (
    AssociationsDealsToCompaniesStream,
    ContactsStream ,
    CompaniesStream,
    DealsStream,
    MeetingsStream,
    OwnersStream,
    PropertiesCompaniesStream,
    PropertiesContactsStream,
    PropertiesDealsStream,
    PropertiesMeetingsStream,
)

from tap_hubspot.marketing_streams import (
    MarketingEmailsStream,
    MarketingCampaignIdsStream,
    MarketingCampaignsStream,
    MarketingFormsStream,
)

STREAM_TYPES = [
    ## CRM
    # AssociationsDealsToCompaniesStream,
    # ContactsStream,
    # CompaniesStream,
    # DealsStream,
    # MeetingsStream,
    # PropertiesCompaniesStream,
    # PropertiesContactsStream,
    # PropertiesDealsStream,
    # PropertiesMeetingsStream,
    # OwnersStream,

    ## Marketing
    MarketingEmailsStream,
    MarketingCampaignIdsStream,
    MarketingCampaignsStream,
    MarketingFormsStream,

]


class TapHubspot(Tap):
    """Hubspot tap class."""
    name = "tap-hubspot"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "access_token",
            th.StringType,
            required=True,
            description="PRIVATE Access Token for Hubspot API",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            required=True,
            description="The earliest record date to sync"
        )
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]

if __name__ == "__main__":
    TapHubspot.cli()
