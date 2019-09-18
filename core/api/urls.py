from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework import routers
from .api import (UserViewSet,DictionaryViewSet,CustomDictionaryViewSet,
	TopicViewSet,SearchViewSet,WordRootViewSet,SocialNetworkAccountsViewSet,
	WordCloudViewSet)
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
router.register('api/search', SearchViewSet, 'search')
router.register('api/social_network_accounts', SocialNetworkAccountsViewSet, 'social_network_accounts')
#router.register('api/wordcloud', WordCloudViewSet, 'wordcloud')

schema_view = get_swagger_view(title='Swagger Topic Analyzer REST API Documentation')

urlpatterns = [
    url(r'^swagger/$', schema_view),
    url(r'^api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
#    url(r'^index/', views.IndexView.as_view(), name='index')    
    url(r'^api/wordcloud/', WordCloudViewSet.as_view({'get': 'list', 'post':'create'}), name='wordcloud'),
    url(r'^api/customdictionary/custom_dictionary_kpi/user/<int:user_id>/language/<int:language_id>', CustomDictionaryViewSet.as_view({'post': 'custom_dictionary_kpi'}), name='custom_dictionary_kpi')
]

urlpatterns += router.urls

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
