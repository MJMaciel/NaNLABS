from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=5)
    title = serializers.CharField(max_length=50, allow_blank=True, default=None)
    description = serializers.CharField(max_length=250, allow_blank=True, default=None)
    category = serializers.CharField(max_length=50, allow_blank=True, default=None)

    def validate(self, data):
        if data['type'] not in ['issue', 'bug', 'task']:
            raise serializers.ValidationError('The type field is invalid.')
        if data['type'] == 'issue' or data['type']  == 'bug':
            if not data.get('description'):
                raise serializers.ValidationError('The description field can not be empty.')
        if data['type']  == 'issue' or data['type']  == 'task':
            if not data['title']:
                raise serializers.ValidationError('The title field can not be empty.')
        if data['type']  == 'task':
            if not data['category']:
                raise serializers.ValidationError('The category field can not be empty.')
        return data
