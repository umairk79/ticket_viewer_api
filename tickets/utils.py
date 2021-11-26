from django.conf import settings

FIELDS_TO_SEND = getattr(settings, "FIELDS_TO_SEND", "")
fields = FIELDS_TO_SEND.split(",")


def process_response(response):
    final_response = {
        "tickets": [{field: ticket[field] for field in fields} for ticket in response["results"]]
    }
    return final_response


