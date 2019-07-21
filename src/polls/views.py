from rest_framework.exceptions import APIException
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from Citadel.helpers import get_int_value
from polls.serializers import PollPaginationSerializer
from second_backend.endpoints import get_polls


class PollListView(APIView):
    def get(self, request):
        limit = get_int_value(request.GET.get('limit'), LimitOffsetPagination.default_limit)
        offset = get_int_value(request.GET.get('offset'))
        is_active = request.GET.get('is_active')

        if is_active:
            is_active = is_active == 'true'

        polls = get_polls(limit, offset, is_active)

        if not polls:
            raise APIException(detail='Невозможно получить ответ от second_backend')

        serializer = PollPaginationSerializer(
            data=polls,
            context={
                'request': request,
                'limit': limit,
                'is_active': is_active,
                'offset': offset
            }
        )
        if not serializer.is_valid():
            raise APIException(detail='Получен некорректный ответ от second_backend')
        return Response(serializer.data)
