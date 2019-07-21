from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from wallet.models.wallet import Wallet

from wallet.serializers.wallet import WalletSerializer, WalletEditSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        qs = super(WalletViewSet, self).get_queryset()
        qs = qs.filter(user=self.request.user)

        return qs

    def create(self, request, *args, **kwargs):
        self.serializer_class = WalletEditSerializer
        return super(WalletViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = WalletEditSerializer
        return super(WalletViewSet, self).update(request, *args, **kwargs)
