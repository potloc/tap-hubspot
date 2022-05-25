from singer_sdk import typing as th  # JSON Schema typing helpers

schema = th.PropertiesList(
    th.Property("objectType", th.StringType),
    th.Property("objectId", th.StringType),
    th.Property("eventType", th.StringType),
    th.Property("occurredAt", th.DateTimeType),
    th.Property("id", th.StringType),
    th.Property("Properties",
        th.ObjectType(
            th.Property("hs_action_execution_index", th.StringType),
            th.Property("hs_flow_id", th.StringType),
            th.Property("hs_action_executed_timestamp", th.StringType),
            th.Property("hs_action_id", th.StringType),
            th.Property("hs_enrollment_id", th.StringType),
            th.Property("hs_delayed_object_type", th.StringType)
        )
    ),
).to_dict()
