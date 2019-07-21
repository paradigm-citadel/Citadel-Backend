from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings

from account.models.account import Account

from account.serializers.auth import RegistrationSerializer, \
    RestorePasswordSerializer

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            new_user = User(
                email=serializer.validated_data.get('email')
            )
            new_user.set_password(serializer.validated_data.get('password'))
            new_user.save()

            Account.objects.create(user=new_user)

            token, created = Token.objects.get_or_create(user=new_user)

        response = Response({
            'token': token.key
        })

        return response


class RestorePasswordView(APIView):
    def post(self, request):
        serializer = RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        user = User.objects.get(email=email)

        new_password = get_random_string(length=10)

        with transaction.atomic():
            user.set_password(new_password)
            user.save()

            send_mail(
                subject='Citadel password restore',
                message=f'Your new password: {new_password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

        response = Response({
            'email': email,
            'status': 'success'
        })

        return response
