from django.urls import path

from . import views

urlpatterns = [
    path('apps/', views.app_list, name='app_list'),
    path('apps/create/', views.create_app, name='create_app'),
    path('apps/<int:id>/', views.get_app, name='get_app'),
    path('apps/<int:id>/delete/', views.delete_app, name='delete_app'),
    path('apps/<int:id>/edit/', views.edit_app, name='edit_app'),
]