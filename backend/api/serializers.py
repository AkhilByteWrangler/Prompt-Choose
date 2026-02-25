from rest_framework import serializers
from .models import Prompt


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'response_a_generated_at', 'response_b_generated_at']


class GenerateResponsesSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True)
    model_name = serializers.CharField(default='gpt-3.5-turbo')
    
    temperature_a = serializers.FloatField(default=0.7, min_value=0.0, max_value=2.0)
    max_tokens_a = serializers.IntegerField(default=500, min_value=10, max_value=2000)
    top_p_a = serializers.FloatField(default=1.0, min_value=0.0, max_value=1.0)
    frequency_penalty_a = serializers.FloatField(default=0.0, min_value=-2.0, max_value=2.0)
    presence_penalty_a = serializers.FloatField(default=0.0, min_value=-2.0, max_value=2.0)
    
    temperature_b = serializers.FloatField(default=0.9, min_value=0.0, max_value=2.0)
    max_tokens_b = serializers.IntegerField(default=500, min_value=10, max_value=2000)
    top_p_b = serializers.FloatField(default=1.0, min_value=0.0, max_value=1.0)
    frequency_penalty_b = serializers.FloatField(default=0.0, min_value=-2.0, max_value=2.0)
    presence_penalty_b = serializers.FloatField(default=0.0, min_value=-2.0, max_value=2.0)


class RecordPreferenceSerializer(serializers.Serializer):
    preference = serializers.ChoiceField(choices=['A', 'B', 'TIE'], required=True)


class TrainingDataSerializer(serializers.Serializer):
    prompt = serializers.CharField()
    chosen = serializers.CharField()
    rejected = serializers.CharField()
    metadata = serializers.DictField()
