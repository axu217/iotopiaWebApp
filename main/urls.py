from django.conf.urls import url
from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='index'),
	url(r'^send/$', views.SendFormView.as_view(), name='send'),
	url(r'^control/$', views.ControlFormView.as_view(), name='control')
]
