
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
    ),
    th.Property("portalId", th.IntegerType),
    th.Property("insertedAt", th.IntegerType),
    th.Property("updatedAt", th.DateTimeType),
    th.Property("creationSource",
        th.ObjectType(
            th.Property("sourceApplication",
                th.ObjectType(
                    th.Property("source", th.StringType),
                    th.Property("serviceName", th.StringType)
                )
            ),
            th.Property("createdByUser",
                th.ObjectType(
                    th.Property("userId", th.IntegerType),
                    th.Property("userEmail", th.StringType),
                )
            ),
            th.Property("createdAt", th.IntegerType)
        ),
    ),
    th.Property("updateSource",
        th.ObjectType(
            th.Property("sourceApplication",
                th.ObjectType(
                    th.Property("source", th.StringType),
                    th.Property("serviceName", th.StringType)
                )
            ),
            th.Property("updatedByUser",
                th.ObjectType(
                    th.Property("userId", th.IntegerType),
                    th.Property("userEmail", th.StringType),
                )
            ),
            th.Property("updatedAt", th.IntegerType)
        ),
    ),
    th.Property("originalAuthorId", th.IntegerType),
    th.Property("contactListIds",
        th.ObjectType(
                th.Property("enrolled", th.IntegerType),
                th.Property("active", th.IntegerType),
                th.Property("completed", th.IntegerType),
                th.Property("succeeded", th.IntegerType),
        )
    ),
    th.Property("description", th.StringType),
    th.Property("type", th.StringType),
    th.Property("enabled", th.BooleanType),
    th.Property("id", th.IntegerType),
    th.Property("name", th.StringType),
).to_dict()
