from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from account.models.account import Account

from account.serializers.account import AccountSerializer, \
    AccountUpdateSerializer, ChangePasswordSerializer


class AccountViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.queryset.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        self.serializer_class = AccountUpdateSerializer
        return super(AccountViewSet, self).update(request, *args, **kwargs)

    @action(detail=True, methods=['put'])
    def change_password(self, request):

        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.check_password(serializer.data.get("old_password")):
            raise ValidationError({'detail': "wrong old_password"})
            # set_password also hashes the password that the user will get
        request.user.set_password(serializer.data.get("new_password"))
        request.user.save()

        Token.objects.filter(user=request.user).delete()
        token = Token.objects.create(user=request.user)

        response = Response({
            'token': token.key
        })

        return response
