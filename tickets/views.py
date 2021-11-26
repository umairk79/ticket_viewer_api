from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class Connect(APIView):

    def post(self, request):
        print(request.POST)
        tickets = ["10320", "10321", "10322", "10820"]
        return Response(tickets)
