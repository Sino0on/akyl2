from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.map_view, name='map'),
    path('driver-tracking/', views.driver_tracking_view, name='driver_tracking'),
    path('bus/<int:pk>/', views.bus_entry_view, name='bus_entry'),
    path('analytics/', views.analytics_view, name='analytics'),

]
