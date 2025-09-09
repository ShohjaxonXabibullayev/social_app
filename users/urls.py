from .views import SignUpView,  VerifyCodeApiView, GetNewCodeVerify, ChangeInfoUserAPi
from django.urls import path

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('verify/', VerifyCodeApiView.as_view()),
    path('new-verify/', GetNewCodeVerify.as_view()),
    path('change-info/', ChangeInfoUserAPi.as_view())
]