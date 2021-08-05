from rest_framework import serializers
from prophecies.core.models import Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'name', 'value', 'require_alternative_value']
