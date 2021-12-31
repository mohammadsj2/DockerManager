from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path('apps/', views.AppList.as_view(), name='app_list'),
    path('apps/create/', views.CreateApp.as_view(), name='create_app'),
    path('apps/<int:app_id>/', views.GetApp.as_view(), name='get_app'),
    path('apps/<int:app_id>/delete/', views.DeleteApp.as_view(), name='delete_app'),
    path('apps/<int:app_id>/edit/', views.EditApp.as_view(), name='edit_app'),
    path('apps/<int:app_id>/containers/', views.ContainerList.as_view(), name='container_list'),
    path('apps/<int:app_id>/containers/create/', views.CreateContainer.as_view(), name='create_container'),
]