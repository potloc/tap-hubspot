from singer_sdk import typing as th  # JSON Schema typing helpers

schema = th.PropertiesList(
    th.Property("id", th.NumberType),
    th.Property("appId", th.NumberType),
    th.Property("appName", th.StringType),
).to_dict()
