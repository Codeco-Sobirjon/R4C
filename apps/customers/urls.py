from django.urls import path
from apps.customers.views import *


urlpatterns = [
    path('login/', CustomAuthTokenView.as_view(), name='login'),
]