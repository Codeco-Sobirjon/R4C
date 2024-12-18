from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone
import pandas as pd
from io import BytesIO
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RobotProductionReport(APIView):
    @swagger_auto_schema(
        operation_description="Generate a production report for robots for the past week. Returns an Excel file with aggregated order data.",
        responses={
            200: openapi.Response('Success', examples={
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'robot_report.xlsx'
            }),
            404: 'No data found or no aggregated data available'
        }
    )
    def get(self, request, *args, **kwargs):
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(weeks=1)

        orders_data = Order.objects.filter(created__range=[start_date, end_date])

        if not orders_data.exists():
            return Response({"message": "No data found for the past week"}, status=404)

        aggregated_data = (
            orders_data
            .values('robot_serial__model', 'robot_serial__version')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('robot_serial__model', 'robot_serial__version')
        )

        report_data = [
            {
                'Модель': entry['robot_serial__model'],
                'Версия': entry['robot_serial__version'],
                'Количество за неделю': entry['total_quantity'] or 0
            }
            for entry in aggregated_data
        ]

        if not report_data:
            return Response({"message": "No aggregated data available"}, status=404)

        df = pd.DataFrame(report_data)

        excel_file = BytesIO()

        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Роботы')

        excel_file.seek(0)
        response = HttpResponse(
            excel_file,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="robot_report.xlsx"'

        return response


create_order_response = openapi.Response(
    description="Order created successfully or robot availability email sent",
    schema=OrderSerializer()
)


class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new order for a robot",
        responses={201: create_order_response, 400: 'Bad Request'},
        request_body=OrderSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()

            robot = order.robot_serial
            if not robot.is_available:
                send_mail(
                    subject=f"Робот модели {robot.model} версии {robot.version} не доступен",
                    message=f"Добрый день!\n\nК сожалению, робот модели {robot.model} версии {robot.version} в данный момент недоступен.\nКак только он станет доступен, мы уведомим вас.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[order.customer.email],
                    fail_silently=False
                )
                order.is_robot_available = False
                order.save()
            else:
                send_mail(
                    subject=f"Ваш заказ на робота модели {robot.model} версии {robot.version}",
                    message=f"Добрый день!\n\nВаш заказ на робота модели {robot.model} версии {robot.version} успешно оформлен и будет доставлен в ближайшее время.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[order.customer.email],
                    fail_silently=False
                )

            return Response({'msg': 'Please check your email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
