from django.urls import path

from . import views

app_name = 'datademo'

urlpatterns = [
    path('api/typescript/', views.typescript_interface, name="ts"),
    path('api/data-demo/', views.DataDemo.as_view(), name='data_demo'),
    path('api/list/', views.List.as_view(), name='list'),
]
