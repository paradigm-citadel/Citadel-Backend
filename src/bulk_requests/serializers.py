from django.http import QueryDict
from django.urls import resolve, Resolver404
from urllib.parse import urlparse

from rest_framework import serializers


class GETEnpointsSerializer(serializers.Serializer):
    url = serializers.CharField()

    def validate(self, validated_data):
        parsed_url = urlparse(validated_data['url'])
        url_no_query_string = parsed_url.path

        try:
            validated_data['view'] = resolve(url_no_query_string).func
        except Resolver404:
            validated_data['view'] = None

        validated_data['url_no_query_string'] = url_no_query_string
        validated_data['query_string'] = parsed_url.query
        validated_data['query_params'] = QueryDict(parsed_url.query)
        return validated_data


class BulkGETSerializer(serializers.Serializer):
    endpoints = GETEnpointsSerializer(many=True)
