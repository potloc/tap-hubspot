from singer_sdk import typing as th  # JSON Schema typing helpers

schema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("name", th.StringType),
    th.Property("createAt", th.DateTimeType),
    th.Property("updatedAt", th.DateTimeType),
    th.Property("archived", th.BooleanType),
    th.Property("fieldGroups",
        th.ArrayType(
            th.ObjectType(
                th.Property("groupType", th.StringType),
                th.Property("richTextType", th.StringType),
                th.Property("fields",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("objectTypeId", th.StringType),
                            th.Property("name", th.StringType),
                            th.Property("required", th.BooleanType),
                            th.Property("hidden", th.BooleanType),
                            th.Property("fieldType", th.StringType),
                        )
                    )
                )
            )
        )
    ),
    th.Property("configuration",
        th.ObjectType(
            th.Property("language", th.StringType),
            th.Property("cloneable", th.BooleanType),
            th.Property("postSubmitAction",
                th.ObjectType(
                    th.Property("type", th.StringType),
                    th.Property("value", th.StringType),
                )
            )
        )
    ),
    th.Property("formType", th.StringType),
).to_dict()
