from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Min, Max

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models.account import Account
from transaction.models.transaction import Transaction


User = get_user_model()


class CurrentAccountDefault(serializers.CurrentUserDefault):
    def __call__(self):
        return self.user.account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
        )

    def validate_email(self, value):
        if not self.instance:
            return value

        is_exist = User.objects.filter(email=value).exclude(
            pk=self.instance.pk
        ).exists()
        if is_exist:
            raise ValidationError('This field must be unique.', code='unique')

        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate_new_password(self, value):
        validate_password(value)
        return value


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    chart_date_from = serializers.SerializerMethodField()
    chart_date_to = serializers.SerializerMethodField()

    def get_chart_date_from(self, account: Account):
        return Transaction.objects.filter(
            wallet__user=account.user
        ).aggregate(
            min=Min('committed')
        ).get('min', None)

    def get_chart_date_to(self, account: Account):
        return Transaction.objects.filter(
            wallet__user=account.user
        ).aggregate(
            max=Max('committed')
        ).get('max', None)

    class Meta:
        model = Account
        fields = (
            'user',
            'chart_date_from',
            'chart_date_to'
        )


class AccountUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Account
        fields = (
            'user',
            'chart_date_from',
            'chart_date_to'
        )

    def update(self, account, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance=account.user, data=user_data)
            user_serializer.is_valid(raise_exception=True)

            email = user_data.get('email')

            if email:
                account.user.email = email

            account.user.save()

        account = super(AccountUpdateSerializer, self).update(
            account, validated_data
        )

        return account
