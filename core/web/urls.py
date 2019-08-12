#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
#from api import views
#from .import views
from .views import (IndexView)

app_name= 'web'

urlpatterns = [
	path('index/', IndexView.as_view(), name='index')
]


#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
