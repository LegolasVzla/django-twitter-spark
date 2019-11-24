from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework import routers
from .api import (UserViewSet,DictionaryViewSet,CustomDictionaryViewSet,
	TopicViewSet,SearchViewSet,WordRootViewSet,SocialNetworkAccountsViewSet,
	WordCloudViewSet)
from rest_framework_swagger.views import get_swagger_view
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
#from api import views

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
    url(r'^api/user/user_details/user/<int:user_id>', UserViewSet.as_view({'post': 'user_details'}), name='user_details'),
    url(r'^api/wordcloud/', WordCloudViewSet.as_view({'get': 'list', 'post':'create'}), name='wordcloud'),
    url(r'^api/customdictionary/custom_dictionary_kpi/user/<int:user_id>/language/<int:language_id>', CustomDictionaryViewSet.as_view({'post': 'custom_dictionary_kpi'}), name='custom_dictionary_kpi'),
    url(r'^api/customdictionary/custom_dictionary_polarity_get/user/<int:user_id>/language/<int:language_id>/word/<string:word>', CustomDictionaryViewSet.as_view({'post': 'custom_dictionary_polarity_get'}), name='custom_dictionary_polarity_get'),
    url(r'^api/customdictionary/custom_dictionary_polarity_create/<int:user_id>/language/<int:language_id>/word/<int:word>/polarity/<string:polarity>', CustomDictionaryViewSet.as_view({'post': 'create'}), name='custom_dictionary_polarity_create'),
    url(r'^api/customdictionary/custom_dictionary_polarity_update/word/<int:word>/polarity/<string:polarity>', CustomDictionaryViewSet.as_view({'put': 'update'}), name='custom_dictionary_polarity_update'),
    url(r'^api/customdictionary/custom_dictionary_polarity_delete/word/<int:word>', CustomDictionaryViewSet.as_view({'delete': 'destroy'}), name='custom_dictionary_polarity_delete'),
    url(r'^api/search/recent_search/user/<int:user_id>/social_network/<int:social_network_id>', SearchViewSet.as_view({'post': 'recent_search'}), name='recent_search'),
    url(r'^api/search/word_details/user/<int:user_id>/social_network/<int:social_network_id>/word/<string:word>', SearchViewSet.as_view({'post': 'word_details'}), name='word_details')
]

urlpatterns += router.urls

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
