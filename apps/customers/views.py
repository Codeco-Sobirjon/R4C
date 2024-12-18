from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import CustomAuthTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from ..robots.utils import check_required_key


class CustomAuthTokenView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=CustomAuthTokenSerializer, tags=['Вход пользователя'])
    def post(self, request, *args, **kwargs):
        valid_fields = {"username", "password"}
        unexpected_fields = check_required_key(request, valid_fields)

        if unexpected_fields:
            return Response(f"Неожиданные поля: {', '.join(unexpected_fields)}", status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomAuthTokenSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
