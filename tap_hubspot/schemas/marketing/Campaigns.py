from singer_sdk import typing as th  # JSON Schema typing helpers

schema = th.PropertiesList(
    th.Property("id", th.IntegerType),
    th.Property("appId", th.IntegerType),
    th.Property("appName", th.StringType),
    th.Property("contentId", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("subject", th.StringType),
    th.Property("counters",
        th.ObjectType(
            th.Property("processed", th.IntegerType),
            th.Property("deferred", th.IntegerType),
            th.Property("bounce", th.IntegerType),
            th.Property("delivered", th.IntegerType),
            th.Property("reply", th.IntegerType),
            th.Property("sent", th.IntegerType),
            th.Property("click", th.IntegerType),
            th.Property("open", th.IntegerType),
        )
    ),
    th.Property("type", th.StringType)
).to_dict()
