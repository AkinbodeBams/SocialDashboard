from django.urls import path
from . import views

urlpatterns = [
    path('get-social-media-dashboard/', views.SocialMediaDashBoardProfile.as_view(),name='get-social-media-dashboard')
]