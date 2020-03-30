from django.urls import path
from . import views
from . import views
from movieTube import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'videos'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
]
urlpatterns += staticfiles_urlpatterns()
