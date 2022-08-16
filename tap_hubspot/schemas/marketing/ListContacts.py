from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("list_id", th.IntegerType),
    th.Property("addedAt", th.IntegerType),
    th.Property("vid", th.IntegerType),
    th.Property("canonical-vid", th.IntegerType),
    th.Property("merged-vids", th.ArrayType(th.ObjectType)),
    th.Property("merge-audits", th.ArrayType(th.ObjectType)),
    th.Property("portal-id", th.IntegerType),
    th.Property("is-contact", th.BooleanType),
    th.Property("properties", th.ObjectType()),
    th.Property("form-submissions", th.ArrayType(
        th.ObjectType
    )),
    th.Property("identity-profiles", th.ArrayType(
        th.ObjectType(
            th.Property("vid", th.IntegerType),
            th.Property("saved-at-timestamp", th.IntegerType),
            th.Property("deleted-changed-timestamp", th.IntegerType),
            th.Property("identities", th.ArrayType(
                th.ObjectType(
                    th.Property("type", th.StringType),
                    th.Property("value", th.StringType),
                    th.Property("timestamp", th.IntegerType),
                )
            )),
        )
    )),
).to_dict()
