from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import path
from api import views

urlpatterns = [
    url(r'^index/', views.IndexView.as_view(), name='index')
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
