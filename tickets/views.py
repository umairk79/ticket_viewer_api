from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework.exceptions import *
from django.conf import settings
from . import utils


# Main /tickets django view class
class Tickets(APIView):
    # Get downstream urls and query params from settings.py configuration file
    ZENDESK_API_URL = getattr(settings, "ZENDESK_API_URL", "")
    ZENDESK_API_QUERY = getattr(settings, "ZENDESK_API_QUERY", "")

    # implementation for post request
    def post(self, request):
        """
        This post call internally calls the zendesk tickets api to fetch tickets.
        Used Email and Password for basic auth.
        Takes subdomain from the user.
        Takes page number as a request parameter for pagination requests.
        Handles all types of exceptions. Returns relevant error responses based on scenarios.
        Return success response based on the fields specified in the global settings configuration file.
        """
        request = request.data['data']
        email, password, subdomain, page_number = request['email'], request['password'], request['subdomain'], request['page']
        page_number_query = "&page=" + str(page_number)
        ZENDESK_API_URL = self.ZENDESK_API_URL.replace("<<subdomain>>", subdomain)

        try:
            response = requests.get(ZENDESK_API_URL + self.ZENDESK_API_QUERY + page_number_query, auth=(email, password))
            response.raise_for_status()
        except requests.exceptions.Timeout:
            return Response({"error": "Timeout while trying to connect with Zendesk"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.TooManyRedirects:
            return Response({"error": "Bad Zendesk URL - Too Many Redirects"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            response = e.response
            if response is not None:
                if "title" in response.json()["error"]:
                    res = {
                        "error": response.json()["error"]["title"]
                    }
                    return Response(res, status=response.status_code)
                return Response(response.json(), status=response.status_code)
            else:
                return Response({"error": "Unknown error"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": "Unknown error"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            response = utils.process_response(response.json())
        except Exception:
            return Response({"error": "Error processing Zendesk API response"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response)

