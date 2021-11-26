from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework.exceptions import *
from django.conf import settings
from . import utils


ZENDESK_API_URL = getattr(settings, "ZENDESK_API_URL", "")
ZENDESK_API_QUERY = getattr(settings, "ZENDESK_API_QUERY", "")


class Connect(APIView):

    def post(self, request):


        request = request.data['data']
        email, password, subdomain = request['email'], request['password'], request['subdomain']

        try:
            response = requests.get("https://" + subdomain + ZENDESK_API_URL + ZENDESK_API_QUERY, auth=(email, password))
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
        except Exception:
            return Response({"error": "Unknown error"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            response = utils.process_response(response.json())
        except Exception:
            return Response({"error": "Error processing Zendesk API response"}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response)

