from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework import routers
from .api import (UserViewSet,DictionariesViewSet,CustomDictionariesViewSet,
	TopicsViewSet,WordRootsViewSet)

router = routers.DefaultRouter()
router.register('api/user', UserViewSet, 'user')
router.register('api/dictionaries', DictionariesViewSet, 'dictionaries')
router.register('api/customdictionaries', CustomDictionariesViewSet, 'customdictionaries')
router.register('api/topics', TopicsViewSet, 'topics')
router.register('api/wordroots', WordRootsViewSet, 'wordroots')

urlpatterns = []

urlpatterns += router.urls

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
