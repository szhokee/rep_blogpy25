from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from applications.account.serializer import RegisterSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Вы успешно зарегистрировались. Вам отправлено письмо с активацией, status=201')


class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.object.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'Успешно'}, status=200)
        except User.DoesNotExist:
            return Response({'Link expired'}, status=400)
