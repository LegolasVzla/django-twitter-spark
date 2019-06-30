from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework import routers
from .api import (UserViewSet,DictionariesViewSet,CustomDictionariesViewSet,
	TopicsViewSet,WordRootsViewSet)
from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter()
router.register('api/user', UserViewSet, 'user')
router.register('api/dictionaries', DictionariesViewSet, 'dictionaries')
router.register('api/customdictionaries', CustomDictionariesViewSet, 'customdictionaries')
router.register('api/topics', TopicsViewSet, 'topics')
router.register('api/wordroots', WordRootsViewSet, 'wordroots')

schema_view = get_swagger_view(title='Swagger DRF-Orientdb-PostgreSQL REST API Documentation')

urlpatterns = [
    url(r'^swagger/$', schema_view)
]

urlpatterns += router.urls

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
