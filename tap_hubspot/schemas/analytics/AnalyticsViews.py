from singer_sdk import typing as th  # JSON Schema typing helpers

schema = th.PropertiesList(
    th.Property("id", th.IntegerType),
    th.Property("title", th.StringType),
    th.Property("createdAt", th.IntegerType),
    th.Property("creatorId", th.IntegerType),
    th.Property("deletedAt", th.IntegerType),
    th.Property("updatedDate", th.DateTimeType),
    th.Property("updaterId", th.IntegerType),
    th.Property("reportPropertyFilters",
        th.ArrayType(
            th.ObjectType(
                th.Property("prop", th.StringType),
                th.Property("op", th.StringType),
                th.Property("args", th.ArrayType(th.StringType))
            )
        )
    ),
    th.Property("containsLegacyReportProperties", th.BooleanType)
).to_dict()
