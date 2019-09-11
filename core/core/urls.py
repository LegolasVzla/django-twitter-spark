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
from web.views import (IndexView,UserProfileView,CustomDictionaryView,
    TwitterSearchView,RecentSearchTwitterView)

urlpatterns = [
    path('admin/', admin.site.urls),
	path('',include('api.urls')),
    path('',include('accounts.urls')),
    url(r'^socialanalyzer/$', IndexView.as_view(), name='web'),
    url(r'^socialanalyzer/profile_get/$', UserProfileView.as_view(), name='profile_get'),
    url(r'^socialanalyzer/profile_update/$', UserProfileView.as_view(), name='profile_update'),
    url(r'^socialanalyzer/twitter_search/$', TwitterSearchView.as_view(), name='twitter_search'),
    url(r'^socialanalyzer/twitter_results/$', TwitterSearchView.as_view(), name='twitter_results'),
    url(r'^socialanalyzer/dictionary_get/$', CustomDictionaryView.as_view(), name='dictionary_get'),
    url(r'^socialanalyzer/dictionary_create/$', CustomDictionaryView.as_view(), name='dictionary_create'),
    url(r'^socialanalyzer/dictionary_update/$', CustomDictionaryView.as_view(), name='dictionary_update'),
    url(r'^socialanalyzer/dictionary_remove/$', CustomDictionaryView.as_view(), name='dictionary_remove'),
    url(r'^socialanalyzer/recent_search_twitter/$', RecentSearchTwitterView.as_view(), name='recent_search_twitter'),
    url(r'^socialanalyzer/timeline_search_twitter/$', RecentSearchTwitterView.as_view(), name='timeline_search_twitter')
]
