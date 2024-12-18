from django.urls import path
from apps.robots.views import *


urlpatterns = [
    path('robots/', RobotListCreateAPIView.as_view(), name='robot-list-create'),
    path('robots/<int:pk>/', RobotDetailAPIView.as_view(), name='robot-detail'),
]
