"""Hubspot tap class."""

from typing import List
# from black import main

from singer_sdk import Tap, Stream
from singer_sdk import typing as th
from tap_hubspot.streams import (
    AssociationsCompaniesToContactsStream,
    AssociationsCompaniesToDealsStream,
    AssociationsContactsToCompaniesStream,
    AssociationsContactsToDealsStream,
    AssociationsDealsToCompaniesStream,
    AssociationsDealsToContactsStream,
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

from tap_hubspot.events_streams import (
    WebAnalyticsContactsStream,
    WebAnalyticsDealsStream
)

from tap_hubspot.analytics_streams import (
    AnalyticsViewsStream,
)

from tap_hubspot.automation_streams import (
    WorkflowsStream,
)


STREAM_TYPES = [
    ## CRM
    AssociationsCompaniesToContactsStream,
    AssociationsCompaniesToDealsStream,
    AssociationsContactsToCompaniesStream,
    AssociationsContactsToDealsStream,
    AssociationsDealsToCompaniesStream,
    AssociationsDealsToContactsStream,
    ContactsStream,
    CompaniesStream,
    ContactsStream,
    DealsStream,
    MeetingsStream,
    PropertiesCompaniesStream,
    PropertiesContactsStream,
    PropertiesDealsStream,
    PropertiesMeetingsStream,
    OwnersStream,

    ## Marketing
    MarketingEmailsStream,
    MarketingCampaignIdsStream,
    MarketingCampaignsStream,
    MarketingFormsStream,

    # Events
    WebAnalyticsContactsStream,
    WebAnalyticsDealsStream,

    ## Analytics
    AnalyticsViewsStream,

    ## Automation
    WorkflowsStream
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
