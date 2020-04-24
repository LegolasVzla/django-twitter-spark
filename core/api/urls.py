from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework import routers
from .api import (UserViewSet,DictionaryViewSet,CustomDictionaryViewSet,
	TopicViewSet,SearchViewSet,WordRootViewSet,SocialNetworkAccountsViewSet,
	WordCloudViewSet,TwitterViewSet,MachineLearningViewSet,BigDataViewSet)
from rest_framework_swagger.views import get_swagger_view
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
#from api import views

router = routers.DefaultRouter()
router.register('api/user', UserViewSet, 'user')
router.register('api/dictionary', DictionaryViewSet, 'dictionary')
router.register('api/customdictionary', CustomDictionaryViewSet, 'customdictionary')
router.register('api/topic', TopicViewSet, 'topic')
router.register('api/word_root', WordRootViewSet, 'word_root')
router.register('api/search', SearchViewSet, 'search')
router.register('api/social_network_accounts', SocialNetworkAccountsViewSet, 'social_network_accounts')
router.register('api/word_cloud', WordCloudViewSet, 'word_cloud')

schema_view = get_swagger_view(title='Swagger Topic Analyzer REST API Documentation')

urlpatterns = [
    url(r'^swagger/$', schema_view),
    url(r'^api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
#    url(r'^index/', views.IndexView.as_view(), name='index')
    url(r'^api/user/profile_update/user/<int:user_id>', UserViewSet.as_view({'put': 'profile_update'}), name='profile_update'),
    url(r'^api/user/user_details/user/<int:user_id>', UserViewSet.as_view({'post': 'user_details'}), name='user_details'),
    url(r'^api/word_cloud/comments/<string:comments>/user_id/<int:user_id>', WordCloudViewSet.as_view({'post':'create'}), name='create'),
    url(r'^api/word_cloud/', WordCloudViewSet.as_view({'get': 'list'}), name='list'),
    url(r'^api/dictionary/dictionary_by_polarity/polarity/<string:polarity>', CustomDictionaryViewSet.as_view({'post': 'dictionary_by_polarity'}), name='dictionary_by_polarity'),
    url(r'^api/customdictionary/custom_dictionary_kpi/user/<int:user_id>/language/<int:language_id>', CustomDictionaryViewSet.as_view({'post': 'custom_dictionary_kpi'}), name='custom_dictionary_kpi'),
    url(r'^api/customdictionary/user_custom_dictionary/user/<int:user_id>/language/<int:language_id>', CustomDictionaryViewSet.as_view({'post': 'user_custom_dictionary'}), name='user_custom_dictionary'),
    url(r'^api/customdictionary/custom_dictionary_polarity_get/word/<string:word>', CustomDictionaryViewSet.as_view({'post': 'custom_dictionary_polarity_get'}), name='custom_dictionary_polarity_get'),
    url(r'^api/customdictionary/custom_dictionary_polarity_create/user/<int:user_id>/language/<int:language_id>/word/<string:word>/polarity/<string:polarity>', CustomDictionaryViewSet.as_view({'post': 'create'}), name='custom_dictionary_polarity_create'),
    url(r'^api/customdictionary/update', CustomDictionaryViewSet.as_view({'put': 'update'}), name='update'),
    url(r'^api/customdictionary/custom_dictionary_polarity_delete/word/<int:word>', CustomDictionaryViewSet.as_view({'delete': 'destroy'}), name='custom_dictionary_polarity_delete'),
    url(r'^api/search/recent_search/user/<int:user_id>/social_network/<int:social_network_id>', SearchViewSet.as_view({'post': 'recent_search'}), name='recent_search'),
    url(r'^api/search/recent_search/user/<int:user_id>/social_network/<int:social_network_id>', SearchViewSet.as_view({'post': 'recent_search'}), name='recent_search'),
    url(r'^api/search/twitter_timeline_polarity/user/<int:user_id>/social_network/<int:social_network_id>/word/<string:word>', SearchViewSet.as_view({'post': 'twitter_timeline_polarity'}), name='twitter_timeline_polarity'),
    url(r'^api/search/twitter_timeline_likes/user/<int:user_id>/social_network/<int:social_network_id>/word/<string:word>', SearchViewSet.as_view({'post': 'twitter_timeline_likes'}), name='twitter_timeline_likes'),
    url(r'^api/search/twitter_timeline_shared/user/<int:user_id>/social_network/<int:social_network_id>/word/<string:word>', SearchViewSet.as_view({'post': 'twitter_timeline_shared'}), name='twitter_timeline_shared'),
    url(r'^api/social_network_accounts/accounts_by_social_network/social_network/<int:social_network_id>', SocialNetworkAccountsViewSet.as_view({'post': 'accounts_by_social_network'}), name='accounts_by_social_network'),
    url(r'^api/twitter_analytics/tweets_get', TwitterViewSet.as_view({'post':'tweets_get'}), name='tweets_get'),
    url(r'^api/word_root/word_roots_by_topic', WordRootViewSet.as_view({'get':'word_roots_by_topic'}), name='word_roots_by_topic'),
    url(r'^api/ml_layer/tweet_topic_classification', MachineLearningViewSet.as_view({'post':'tweet_topic_classification'}), name='tweet_topic_classification'),
    url(r'^api/ml_layer/twitter_sentiment_analysis', MachineLearningViewSet.as_view({'post':'twitter_sentiment_analysis'}), name='twitter_sentiment_analysis'),
    url(r'^api/big_data_layer/process_tweets/social_network/<int:social_network_id>', BigDataViewSet.as_view({'post':'process_tweets'}), name='process_tweets'),
    url(r'^api/big_data_layer/twitter_search/text/<string:text>', BigDataViewSet.as_view({'post':'twitter_search'}), name='twitter_search')
]

urlpatterns += router.urls

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
