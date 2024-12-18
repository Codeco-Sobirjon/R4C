from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from apps.robots.models import Robot
from apps.robots.serializers import RobotSerializer, RobotCreateSerializer
from apps.robots.utils import check_required_key


class RobotListCreateAPIView(APIView):
    @swagger_auto_schema(
        tags=['Роботы'],
        operation_description="Получить список всех роботов или создать нового робота",
        responses={200: RobotSerializer(many=True), 201: RobotSerializer()},
    )
    def get(self, request):
        robots = Robot.objects.all()
        serializer = RobotSerializer(robots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['Роботы'],
        request_body=RobotCreateSerializer,
        operation_description="Создать нового робота",
        responses={201: RobotCreateSerializer()},
    )
    def post(self, request):
        valid_fields = {"serial", "model", "version"}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return Response(f"Неожиданные поля: {', '.join(unexpected_fields)}", status=status.HTTP_400_BAD_REQUEST)

        serializer = RobotCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RobotDetailAPIView(APIView):
    @swagger_auto_schema(
        tags=['Роботы'],
        operation_description="Получить робота по ID",
        responses={200: RobotSerializer(), 404: 'Не найдено'},
    )
    def get(self, request, *args, **kwargs):
        robot = get_object_or_404(Robot, id=kwargs.get('id'))
        serializer = RobotSerializer(robot)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['Роботы'],
        request_body=RobotSerializer,
        operation_description="Обновить данные робота по ID",
        responses={200: RobotCreateSerializer(), 404: 'Не найдено'},
    )
    def put(self, request, *args, **kwargs):
        valid_fields = {"serial", "model", "version"}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return Response(f"Неожиданные поля: {', '.join(unexpected_fields)}", status=status.HTTP_400_BAD_REQUEST)

        robot = get_object_or_404(Robot, id=kwargs.get('id'))
        serializer = RobotCreateSerializer(robot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Роботы'],
        operation_description="Удалить робота по ID",
        responses={204: 'Нет содержания', 404: 'Не найдено'},
    )
    def delete(self, request, *args, **kwargs):
        robot = get_object_or_404(Robot, id=kwargs.get('id'))
        robot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

