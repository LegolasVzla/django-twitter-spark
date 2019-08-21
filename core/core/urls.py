"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from web.views import (IndexView,UserProfileView)

urlpatterns = [
    path('admin/', admin.site.urls),
	path('',include('api.urls')),
	#path('',include('web.urls'))
    url(r'^socialanalyzer/$', IndexView.as_view(), name='web'),
    url(r'^socialanalyzer/profile_get/$', UserProfileView.as_view(), name='profile_get'),
    url(r'^socialanalyzer/profile_update/$', UserProfileView.as_view(), name='profile_update')
]
