from rest_framework.response import Response
from rest_framework.views import APIView


class SomeAPI(APIView):
    def get(self, request):
        # Для проверки корректности передачи query-параметров
        if request.query_params.get('logic-query'):
            data = 'yes'
        else:
            data = 'no'
        return Response({'result': data})


class AnotherAPI(APIView):
    def get(self, request):
        return Response({'result': 'hello'})
