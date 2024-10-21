from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .services.google import GoogleAuthService
from .serializers import LoginSerializer, RegisterSerializer, ProfileSerializer

User = get_user_model()


class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]
    google_auth_service = GoogleAuthService()

    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        access_token = self.google_auth_service.get_user_token(code)
        user_info = self.google_auth_service.get_user_info(access_token)

        user = User.objects.filter(email=user_info["email"]).first()
        if not user:
            user = User.objects.create_user(
                email=user_info["email"],
                name=user_info["name"],
                picture=user_info["picture"],
                password="",
                provider="GOOGLE",
            )

        response = {
            "access": str(AccessToken.for_user(user)),
            "refresh": str(RefreshToken.for_user(user)),
        }
        return Response(status=status.HTTP_200_OK, data=response)


class SignInView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        response = {
            "access": str(AccessToken.for_user(user)),
            "refresh": str(RefreshToken.for_user(user)),
        }
        return Response(status=status.HTTP_200_OK, data=response)


class SignUpView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        response = {
            "access": str(AccessToken.for_user(user)),
            "refresh": str(RefreshToken.for_user(user)),
        }
        return Response(status=status.HTTP_201_CREATED, data=response)


class ProfileView(APIView):
    serializer_class = ProfileSerializer

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
