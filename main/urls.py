from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='index'),
    url(r'^graphs/$', views.GraphsView.as_view(), name='graphs')
]
