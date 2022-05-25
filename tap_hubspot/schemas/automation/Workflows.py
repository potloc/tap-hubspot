
from singer_sdk import typing as th  # JSON Schema typing helpers

schema = th.PropertiesList(
    th.Property("migrationStatus",
        th.ObjectType(
            th.Property("portalId", th.IntegerType),
            th.Property("flowId", th.IntegerType),
            th.Property("workflowId", th.IntegerType),
            th.Property("migrationStatus", th.StringType),
            th.Property("enrollmentMigrationStatus", th.StringType),
            th.Property("platformOwnsActions", th.BooleanType),
            th.Property("lastSuccessfulMigrationTimestamp", th.IntegerType)
        )
    )
).to_dict()


# {
#             "migrationStatus": {
#                 "portalId": 2851660,
#                 "flowId": 14601641,
#                 "workflowId": 3130639,
#                 "migrationStatus": "EXECUTION_MIGRATED",
#                 "enrollmentMigrationStatus": "CLASSIC_OWNED",
#                 "platformOwnsActions": true,
#                 "lastSuccessfulMigrationTimestamp": 1576368463600
#             },
#             "portalId": 2851660,
#             "insertedAt": 1530711782341,
#             "updatedAt": 1635366059897,
#             "creationSource": {
#                 "sourceApplication": {
#                     "source": "WORKFLOWS_APP",
#                     "serviceName": "https://app.hubspot.com/workflows/2851660/create"
#                 },
#                 "createdByUser": {
#                     "userId": 4478465,
#                     "userEmail": "ferdinand@potloc.com"
#                 },
#                 "createdAt": 1530711782307
#             },
#             "updateSource": {
#                 "sourceApplication": {
#                     "source": "DIRECT_API",
#                     "serviceName": "AutomationPlatformService-userweb"
#                 },
#                 "updatedByUser": {
#                     "userId": 25273227,
#                     "userEmail": "nelly.harb@potloc.com"
#                 },
#                 "updatedAt": 1635366059897
#             },
#             "originalAuthorUserId": 4478465,
#             "contactListIds": {
#                 "enrolled": 750,
#                 "active": 751,
#                 "completed": 752,
#                 "succeeded": 753
#             },
#             "personaTagIds": [],
#             "lastUpdatedByUserId": 25273227,
#             "contactCounts": {
#                 "active": 0,
#                 "enrolled": 366
#             },
#             "description": "",
#             "type": "DRIP_DELAY",
#             "enabled": false,
#             "id": 3130639,
#             "name": "[FUNNEL] From MQL to SQL"
#         },
