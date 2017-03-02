from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^getChartData/', views.ChartView.as_view()),
]