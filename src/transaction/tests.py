import pprint

from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from transaction.models import Transaction
from wallet.models import Wallet, User, Currency, Rate


class TransactionTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = mommy.make(User)
        cls.currency = mommy.make(Currency)
        mommy.make(Rate, currency=cls.currency, usd=False, btc=False)

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_get_transactions_filter_by_wallet(self):
        wallet1 = mommy.make(Wallet, user=self.user, currency=self.currency)
        wallet2 = mommy.make(Wallet, user=self.user, currency=self.currency)

        transaction1 = mommy.make(Transaction, wallet=wallet1)
        transaction2 = mommy.make(Transaction, wallet=wallet1)
        transaction3 = mommy.make(Transaction, wallet=wallet2)

        url = reverse('transaction-list')
        response = self.client.get(url, {'wallet': wallet1.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(
            [object['pk'] for object in response.data['results']],
            [transaction1.pk, transaction2.pk]
        )
