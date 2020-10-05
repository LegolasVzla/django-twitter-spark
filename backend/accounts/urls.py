#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
#from django.urls import path
from accounts.views import (LoginView, LogoutView)

#app_name= 'accounts'

urlpatterns = [
    #session login
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout')
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)