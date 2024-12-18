from django.urls import path
from apps.orders.views import RobotProductionReport, OrderCreateAPIView

urlpatterns = [
    path('robot-summary-report/', RobotProductionReport.as_view(), name='robot-summary-report'),
    path('orders/', OrderCreateAPIView.as_view(), name='order-create'),
]
