"""
URL configuration for iss_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from driveway_data import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('parking_spot/<int:spot_id>/', views.ParkingSpotView.GetId.as_view()),
    path('parking_spot/', views.ParkingSpotView.Post.as_view()),
    path('parking_spot_actions/', views.ParkingSpotActionsView.GetActionEnum.as_view()),
    path('driveway_entry/<int:entry_id>/', views.DrivewayEntryView.Get.as_view()),
    path('parking_spot/<int:spot_id>/new_entry/', views.DrivewayEntryView.Post.as_view()),
    path('parking_spot/<int:spot_id>/delete_all/', views.DrivewayEntryView.Delete.as_view()),
    path('parking_spot/<int:spot_id>/all_entries/', views.DrivewayEntryView.Get.as_view()),
]
