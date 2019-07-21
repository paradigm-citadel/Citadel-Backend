from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bulk_requests.serializers import BulkGETSerializer


class BulkGETView(APIView):
    def post(self, request):
        serializer = BulkGETSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        endpoints_data = []
        for endpoint_data in serializer.validated_data['endpoints']:
            if not endpoint_data['view']:
                endpoints_data.append({
                    'url': endpoint_data['url'],
                    'http_code': status.HTTP_404_NOT_FOUND,
                    'response_body': {}
                })
                continue

            endpoint_request = HttpRequest()
            # Для корректного тестирования при client.force_authenticate()
            if hasattr(request, '_force_auth_user'):
                endpoint_request._force_auth_user = request._force_auth_user

            endpoint_request.method = 'GET'
            endpoint_request.META = request.META
            endpoint_request.META['PATH_INFO'] = endpoint_data['url_no_query_string']
            endpoint_request.META['QUERY_STRING'] = endpoint_data['query_string']
            endpoint_request.GET = endpoint_data['query_params']

            response = endpoint_data['view'](endpoint_request)
            endpoints_data.append({
                'url': endpoint_data['url'],
                'http_code': response.status_code,
                'response_body': response.data
            })
        return Response(data={'endpoints': endpoints_data})
