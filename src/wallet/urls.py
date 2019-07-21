from rest_framework import routers

from wallet.views.wallet import WalletViewSet
from wallet.views.currency import CurrencyViewSet

router = routers.SimpleRouter()
router.register('wallet', WalletViewSet)
router.register('currency', CurrencyViewSet)
urlpatterns = router.urls
