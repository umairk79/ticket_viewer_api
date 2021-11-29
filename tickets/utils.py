from django.conf import settings

FIELDS_TO_SEND = getattr(settings, "FIELDS_TO_SEND", "")
fields = FIELDS_TO_SEND.split(",")


# Function to extract required fields from the zendesk API response. The fields are specified in the settings file.
def process_response(response):
    final_response = {"tickets": [{field: ticket[field] for field in fields} for ticket in response["tickets"]],
                      "count": response["count"]}
    return final_response


