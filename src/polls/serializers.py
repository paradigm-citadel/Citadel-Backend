from django.utils.http import urlencode
from rest_framework import serializers
from rest_framework.reverse import reverse

from second_backend.serializers import TimestampField


class PollAnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    vote_count = serializers.IntegerField()


class PollSerializer(serializers.Serializer):
    # ToDo: уточнить у second_backend точно ли char
    originalId = serializers.CharField(write_only=True)
    id = serializers.SerializerMethodField()

    title = serializers.CharField()
    net = serializers.CharField()
    start_datetime = TimestampField()
    end_datetime = TimestampField()
    answers = PollAnswerSerializer(many=True)

    def get_id(self, instance):
        return instance['originalId']


class PollPaginationSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = PollSerializer(many=True)
    next = serializers.SerializerMethodField()
    previous = serializers.SerializerMethodField()

    def get_next(self, value):
        limit = self.context['limit']
        offset = self.context['limit']
        is_active = self.context['is_active']

        if limit + offset >= value['count']:
            return None

        next_offset = offset + limit
        base_url = reverse('poll-list', request=self.context['request'])
        query_params = {
            'limit': limit,
            'offset': next_offset,
            'is_active': str(is_active).lower(),
        }
        return f'{base_url}?{urlencode(query_params)}'

    def get_previous(self, value):
        limit = self.context['limit']
        offset = self.context['offset']
        is_active = self.context['is_active']

        if not offset:
            return None

        previous_offset = offset - limit

        base_url = reverse('poll-list', request=self.context['request'])
        query_params = {
            'limit': limit,
            'is_active': str(is_active).lower(),
        }

        if previous_offset <= 0:
            query_params['offset'] = previous_offset
        return f'{base_url}?{urlencode(query_params)}'
