from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from .views import SignInView, SignUpView, GoogleCallbackView, ProfileView

urlpatterns = [
    path("api/token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("google/callback/", GoogleCallbackView.as_view(), name="google-callback"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
