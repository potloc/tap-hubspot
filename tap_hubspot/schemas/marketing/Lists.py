from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("ListId", th.IntegerType),
    th.Property("name", th.StringType),
    th.Property("createAt", th.IntegerType),
    th.Property("updatedAt", th.IntegerType),
    th.Property("dynamic", th.BooleanType),
    th.Property(
        "filters",
        th.ArrayType(
            th.ArrayType(
                th.ObjectType(
                    th.Property("filterFamily", th.StringType),
                    th.Property("withinTimeMode", th.StringType),
                    th.Property("checkPastVersions", th.BooleanType),
                    th.Property("type", th.StringType),
                    th.Property("property", th.StringType),
                    th.Property("value", th.StringType),
                    th.Property("operator", th.StringType),
                )
            )
        )
    ),
    th.Property(
        "metaData",
        th.ObjectType(
            th.Property("processing", th.StringType),
            th.Property("size", th.StringType),
            th.Property("error", th.StringType),
            th.Property("lastProcessingStateChangeAt", th.IntegerType),
            th.Property("lastSizeChangeAt", th.IntegerType),
        )
    ),
    th.Property("portalId", th.IntegerType),
    th.Property("listType", th.StringType),
    th.Property("internalListId", th.IntegerType),
    th.Property("deleteable", th.BooleanType)
).to_dict()
