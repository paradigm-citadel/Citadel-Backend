from django.contrib.auth import password_validation as dj_pswd, get_user_model

from account.models.account import Account

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import NotFound


User = get_user_model()
DRF_UNIQ_USER = UniqueValidator(queryset=User.objects.all())
DRF_UNIQ_ACCOUNT = UniqueValidator(queryset=Account.objects.all())


class RegistrationSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    email = serializers.EmailField(max_length=150, validators=[DRF_UNIQ_USER])
    password = serializers.CharField(validators=[dj_pswd.MinimumLengthValidator])


class RestorePasswordSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    email = serializers.CharField()

    def validate_email(self, value):
        # check User.username because Account.email = User.username
        # see register and update views
        if not User.objects.filter(email=value).count():
            raise NotFound(detail=f'user with email {value} not found')

        return value
