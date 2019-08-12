from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework import routers
from .api import (UserViewSet,DictionaryViewSet,CustomDictionaryViewSet,
	TopicViewSet,WordRootViewSet)
from rest_framework_swagger.views import get_swagger_view
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from api import views

router = routers.DefaultRouter()
router.register('api/user', UserViewSet, 'user')
router.register('api/dictionary', DictionaryViewSet, 'dictionary')
router.register('api/customdictionary', CustomDictionaryViewSet, 'customdictionary')
router.register('api/topic', TopicViewSet, 'topic')
router.register('api/wordroot', WordRootViewSet, 'wordroot')


schema_view = get_swagger_view(title='Swagger DRF-Orientdb-PostgreSQL REST API Documentation')

urlpatterns = [
    url(r'^swagger/$', schema_view),
    url(r'^api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
#    url(r'^index/', views.IndexView.as_view(), name='index')
]

urlpatterns += router.urls

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
