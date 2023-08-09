from singer_sdk import typing as th  # JSON Schema typing helpers

schema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("email", th.StringType),
    th.Property("firstName", th.StringType),
    th.Property("lastName", th.StringType),
    th.Property("userId", th.IntegerType),
    th.Property("createdAt", th.StringType),
    th.Property("updatedAt", th.StringType),
    th.Property("archived", th.BooleanType),
    th.Property(
        "teams", 
        th.ArrayType(
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("primary", th.BooleanType)
            )
        )
    )
).to_dict()
