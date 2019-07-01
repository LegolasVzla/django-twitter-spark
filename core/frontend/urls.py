from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework import routers
from .api import (UserViewSet,DictionaryViewSet,CustomDictionaryViewSet,
	TopicViewSet,WordRootViewSet)
from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter()
router.register('api/user', UserViewSet, 'user')
router.register('api/dictionary', DictionaryViewSet, 'dictionary')
router.register('api/customdictionary', CustomDictionaryViewSet, 'customdictionary')
router.register('api/topic', TopicViewSet, 'topic')
router.register('api/wordroot', WordRootViewSet, 'wordroot')

schema_view = get_swagger_view(title='Swagger DRF-Orientdb-PostgreSQL REST API Documentation')

urlpatterns = [
    url(r'^swagger/$', schema_view)
]

urlpatterns += router.urls

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
