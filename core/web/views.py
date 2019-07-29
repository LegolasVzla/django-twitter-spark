from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.http import (HttpResponse, HttpResponseForbidden, 
	HttpResponseRedirect)
#from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
#from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.models import (User,Language,Dictionary,CustomDictionary,
	SocialNetwork,Searched,Topic,WordRoot)

import json
import requests

# Create your views here.
class IndexView(APIView):

    def get(self, request, *args, **kwargs):
        content = {}
        content['message'] = 'Hello Social Analyzer!'

        return render(request, 'index.html',content)
