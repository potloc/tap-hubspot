from singer_sdk import typing as th  # JSON Schema typing helpers

schema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("name", th.StringType),
    th.Property("createdAt", th.DateTimeType),
    th.Property("updatedAt", th.DateTimeType),
    th.Property("archived", th.BooleanType),
    th.Property("fieldGroups",
        th.CustomType({"anyOf": [{"type": "string"}, {"type": "null"}, {"type:": "array"}]})
        # todo: doesn't play well with flattening
        # th.ArrayType(
        #     th.ObjectType(
        #         th.Property("groupType", th.StringType),
        #         th.Property("richTextType", th.StringType),
        #         th.Property("fields",
        #             th.ArrayType(
        #                 th.ObjectType(
        #                     th.Property("objectTypeId", th.StringType),
        #                     th.Property("name", th.StringType),
        #                     th.Property("required", th.BooleanType),
        #                     th.Property("hidden", th.BooleanType),
        #                     th.Property("fieldType", th.StringType),
        #                 )
        #             )
        #         )
        #     )
        # )
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
    th.Property("displayOptions", th.ObjectType(
        th.Property("cssClass", th.StringType),
        th.Property("renderRawHtml", th.BooleanType),
        th.Property("style", th.ObjectType(
            th.Property("backgroundWidth", th.StringType),
            th.Property("fontFamily", th.StringType),
            th.Property("helpTextColor", th.StringType),
            th.Property("helpTextSize", th.StringType),
            th.Property("labelTextColor", th.StringType),
            th.Property("labelTextSize", th.StringType),
            th.Property("legalConsentTextColor", th.StringType),
            th.Property("legalConsentTextSize", th.StringType),
            th.Property("submitAlignment", th.StringType),
            th.Property("submitColor", th.StringType),
            th.Property("submitFontColor", th.StringType),
            th.Property("submitSize", th.StringType),
        )),
        th.Property("submitButtonText", th.StringType),
        th.Property("theme", th.StringType),
    )),
    th.Property("legalConsentOptions", th.ObjectType(
        th.Property("communicationConsentText", th.StringType),
        th.Property("communicationsCheckboxes",
            th.CustomType({"anyOf": [{"type": "string"}, {"type": "null"}, {"type:": "array"}]})
            # todo: doesn't play well with flattening
            # th.ArrayType(
            #     th.ObjectType(
            #         th.Property("label", th.StringType),
            #         th.Property("required", th.BooleanType),
            #         th.Property("subscriptionTypeId", th.IntegerType),
            #     )
            # )
        ),
        th.Property("consentToProcessText", th.StringType),
        th.Property("privacyText", th.StringType),
        th.Property("type", th.StringType),
    )),
).to_dict()
