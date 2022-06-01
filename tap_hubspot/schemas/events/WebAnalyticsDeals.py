from singer_sdk import typing as th  # JSON Schema typing helpers

schema = th.PropertiesList(
    th.Property("objectType", th.StringType),
    th.Property("objectId", th.StringType),
    th.Property("eventType", th.StringType),
    th.Property("occurredAt", th.DateTimeType),
    th.Property("id", th.StringType),
    th.Property("properties",
        th.ObjectType(
            th.Property("hs_list_id", th.StringType),
            th.Property("hs_object_seg_source", th.StringType),
            th.Property("hs_first_added_timestamp", th.StringType),
            th.Property("hs_list_change_status", th.StringType),
        )
    ),
).to_dict()
