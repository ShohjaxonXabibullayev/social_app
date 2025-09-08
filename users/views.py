from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import render
from .serializers import SignUpSerializer
from .models import CustomUser, CODE_VERIFIED, NEW, VIA_PHONE, VIA_EMAIL
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class SignUpView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny, ]


class VerifyCodeApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        code = self.request.data.get('code')
        user = self.request.user

        self.chech_verify(user, code)

        data = {
            'success': True,
            'code_status': user.verify_codes.filter(code=code).first().code_status,
            "auth_status": user.auth_status,
            "access_token": user.token()["access"],
            "refresh_token": user.token()["refresh_token"]
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @staticmethod
    def chech_verify(user, code):
        verify = user.verify_codes.filter(code=code, code_status=False, expiration_time__gte=datetime.now())
        if not verify.exists():
            data = {
                'success': False,
                'msg': "kodingiz eskirgan yoki xato"
            }
            raise ValidationError(data)
        else:
            verify.update(code_status=True)

        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()




        return True



class GetNewCodeVerify(APIView):

    def get(self, request, *args, **kwargs):
        user = self.request.user

        self.check_verification(user)
        if user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            print(f"VIA_PHONE CODE {code}")
        elif user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            print(f"VIA_EMAIL CODE {code}")
        else:
            raise ValidationError("Telefon yoki email xato")


        data = {
            'status': status.HTTP_200_OK,
            'msg': "Kod email/phone ga yuborildi",
            "access_token": user.token()["access"],
            "refresh_token": user.token()["refresh_token"]
        }
        return Response(data)



    @staticmethod
    def check_verification(user):
        verify = user.verify_codes.filter(expiration_time__gte=datetime.now(), code_status=False)
        if verify.exists():
            data = {
                "msg": "Sizda aktiv kod bor, shundan foydalaning yoki keyinroq yangi kod oling",
                'status':status.HTTP_400_BAD_REQUEST
            }




