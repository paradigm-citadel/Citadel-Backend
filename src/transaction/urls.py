from rest_framework import routers

from transaction.views import TransactionViewSet

router = routers.SimpleRouter()
router.register('transaction', TransactionViewSet)
urlpatterns = router.urls
