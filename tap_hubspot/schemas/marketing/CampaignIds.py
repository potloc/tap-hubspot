from singer_sdk import typing as th  # JSON Schema typing helpers

schema = th.PropertiesList(
    th.Property("id", th.IntegerType),
    th.Property("appId", th.IntegerType),
    th.Property("appName", th.StringType),
).to_dict()
