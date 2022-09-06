"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_standard_tap_tests

from tap_hubspot.tap import TapHubspot

SAMPLE_CONFIG = {
    "access_token": "accesstoken",
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests(requests_mock):
    """Run standard tap tests from the SDK."""
    for stream in ["contacts", "companies", "deals", "meetings"]:
        requests_mock.get(
            f"https://api.hubapi.com/crm/v3/properties/{stream}",
            json={"results": [{"name": "propertyname", "type": "propertytype"}]},
        )

    streams1 = [
        "https://api.hubapi.com/analytics/v2/views?limit=100",
        "https://api.hubapi.com/email/public/v1/campaigns/by-id?limit=100&orderBy=created",
        "https://api.hubapi.com/crm/v3/objects/companies?limit=100&properties=propertyname&archived=True",
        "https://api.hubapi.com/crm/v3/objects/companies?limit=100&properties=propertyname&archived=False",
        "https://api.hubapi.com/crm/v3/objects/contacts?limit=100&properties=propertyname&archived=True",
        "https://api.hubapi.com/crm/v3/objects/contacts?limit=100&properties=propertyname&archived=False",
        "https://api.hubapi.com/crm/v3/objects/deals?limit=100&properties=propertyname&archived=True",
        "https://api.hubapi.com/crm/v3/objects/deals?limit=100&properties=propertyname&archived=False",
        "https://api.hubapi.com/marketing/v3/forms/?limit=100",
        "https://api.hubapi.com/crm/v3/objects/meetings?limit=100&properties=propertyname",
        "https://api.hubapi.com/crm/v3/owners?limit=100",
    ]
    for s in streams1:
        requests_mock.get(
            s,
            json=[{"id": "1", "updatedDate": "2018-08-07"}],
        )

    streams2 = [
        "https://api.hubapi.com/marketing-emails/v1/emails/with-statistics?limit=100&offset=100&orderBy=created",
        "https://api.hubapi.com/automation/v3/workflows?limit=100",
        "https://api.hubapi.com/marketing/v3/forms/?count=100&formTypes=all",
        "https://api.hubapi.com/contacts/v1/lists?limit=100&count=100&offset=0",
    ]
    for s in streams2:
        requests_mock.get(
            s,
            json={
                "total": 1,
                "objects": [{"updated": 1553538703608}],
                "workflows": [{"updatedAt": 1467737836223}],
            },
        )
    tests = get_standard_tap_tests(TapHubspot, config=SAMPLE_CONFIG)
    for test in tests:
        test()
