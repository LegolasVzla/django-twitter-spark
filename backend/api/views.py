from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class IndexView(APIView):

    def get(self, request):
        content = {'message': 'Welcome!'}
        return Response(content)

    def post(self, request):
        content = {'message': 'Welcome!'}
        return Response(content)