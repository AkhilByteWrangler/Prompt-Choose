from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.http import JsonResponse
from bson import ObjectId
from .models import Prompt
from .serializers import (
    PromptSerializer, 
    GenerateResponsesSerializer,
    RecordPreferenceSerializer,
    TrainingDataSerializer
)
from .llm_service import generate_two_responses
import json
import sys


class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    lookup_field = 'pk'  # Use pk which maps to _id since it's the primary key
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        
        try:
            # Convert string pk to ObjectId for MongoDB
            if isinstance(pk, str):
                try:
                    pk = ObjectId(pk)
                except Exception as e:
                    from rest_framework.exceptions import NotFound
                    raise NotFound(f'Invalid ObjectId format: {pk}')
            
            obj = Prompt.objects.get(_id=pk)
            return obj
        except Prompt.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound(f'Prompt not found with id: {pk}')
        except Exception as e:
            from rest_framework.exceptions import NotFound
            raise NotFound(f'Error finding prompt: {str(e)}')
    
    @action(detail=False, methods=['post'], url_path='generate')
    def generate(self, request):
        serializer = GenerateResponsesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        prompt_text = serializer.validated_data['prompt']
        model_name = serializer.validated_data.get('model_name', 'gpt-3.5-turbo')
        
        temperature_a = serializer.validated_data.get('temperature_a', 0.7)
        max_tokens_a = serializer.validated_data.get('max_tokens_a', 500)
        top_p_a = serializer.validated_data.get('top_p_a', 1.0)
        frequency_penalty_a = serializer.validated_data.get('frequency_penalty_a', 0.0)
        presence_penalty_a = serializer.validated_data.get('presence_penalty_a', 0.0)
        
        temperature_b = serializer.validated_data.get('temperature_b', 0.9)
        max_tokens_b = serializer.validated_data.get('max_tokens_b', 500)
        top_p_b = serializer.validated_data.get('top_p_b', 1.0)
        frequency_penalty_b = serializer.validated_data.get('frequency_penalty_b', 0.0)
        presence_penalty_b = serializer.validated_data.get('presence_penalty_b', 0.0)
        
        try:
            response_a, response_b = generate_two_responses(
                prompt_text,
                model_name=model_name,
                temperature_a=temperature_a,
                max_tokens_a=max_tokens_a,
                top_p_a=top_p_a,
                frequency_penalty_a=frequency_penalty_a,
                presence_penalty_a=presence_penalty_a,
                temperature_b=temperature_b,
                max_tokens_b=max_tokens_b,
                top_p_b=top_p_b,
                frequency_penalty_b=frequency_penalty_b,
                presence_penalty_b=presence_penalty_b
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            error_msg = str(e)
            
            # Provide more specific error messages based on the error type
            if 'authentication' in error_msg.lower() or 'api key' in error_msg.lower() or 'unauthorized' in error_msg.lower():
                error_response = 'Invalid API key. Please check your OpenAI API key configuration.'
            elif 'quota' in error_msg.lower() or 'billing' in error_msg.lower():
                error_response = 'OpenAI API quota exceeded. Please check your billing status.'
            elif 'rate limit' in error_msg.lower():
                error_response = 'Rate limit exceeded. Please try again in a moment.'
            elif 'model' in error_msg.lower():
                error_response = f'Model error: {model_name} may not be available.'
            else:
                error_response = f'Error generating responses: {error_msg[:100]}'
            
            return Response(
                {'error': error_response},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Create minimal prompt object to avoid djongo datetime parsing issues
        prompt_obj = Prompt(
            prompt_text=prompt_text,
            response_a=response_a,
            response_b=response_b,
            model_name=model_name,
            temperature=(temperature_a + temperature_b) / 2,
            temperature_a=temperature_a,
            max_tokens_a=max_tokens_a,
            top_p_a=top_p_a,
            frequency_penalty_a=frequency_penalty_a,
            presence_penalty_a=presence_penalty_a,
            temperature_b=temperature_b,
            max_tokens_b=max_tokens_b,
            top_p_b=top_p_b,
            frequency_penalty_b=frequency_penalty_b,
            presence_penalty_b=presence_penalty_b
        )
        
        # Use raw MongoDB insert with all fields including datetime
        from django.db import connection
        from bson import ObjectId
        now = timezone.now()
        
        connection.ensure_connection()
        db = connection.connection.database
        collection = db['api_prompt']
        
        # Generate ObjectId and insert directly
        object_id = ObjectId()
        collection.insert_one({
            '_id': object_id,
            'prompt_text': prompt_text,
            'response_a': response_a,
            'response_b': response_b,
            'model_name': model_name,
            'temperature': (temperature_a + temperature_b) / 2,
            'temperature_a': temperature_a,
            'max_tokens_a': max_tokens_a,
            'top_p_a': top_p_a,
            'frequency_penalty_a': frequency_penalty_a,
            'presence_penalty_a': presence_penalty_a,
            'temperature_b': temperature_b,
            'max_tokens_b': max_tokens_b,
            'top_p_b': top_p_b,
            'frequency_penalty_b': frequency_penalty_b,
            'presence_penalty_b': presence_penalty_b,
            'response_a_generated_at': now,
            'response_b_generated_at': now,
            'preference': None,
            'preference_recorded_at': None,
            'created_at': now,
            'updated_at': now
        })
        
        # Verify object was created and is accessible via Django ORM
        try:
            Prompt.objects.get(_id=object_id)
        except Prompt.DoesNotExist:
            from django.db import reset_queries
            reset_queries()
        
        return Response({
            'id': str(object_id),
            'prompt': prompt_text,
            'response_a': response_a,
            'response_b': response_b,
            'model_name': model_name,
            'temperature': (temperature_a + temperature_b) / 2,
            'temperature_a': temperature_a,
            'temperature_b': temperature_b,
            'created_at': now.isoformat()
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_path='record-preference')
    def record_preference(self, request, pk=None):
        # Verify object exists
        prompt_obj = self.get_object()
        serializer = RecordPreferenceSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        preference = serializer.validated_data['preference']
        now = timezone.now()
        
        # Use raw MongoDB update to avoid djongo datetime parsing issues
        from django.db import connection
        from bson import ObjectId
        
        connection.ensure_connection()
        db = connection.connection.database
        collection = db['api_prompt']
        
        # Convert pk to ObjectId if needed
        object_id = ObjectId(pk) if isinstance(pk, str) else pk
        
        collection.update_one(
            {'_id': object_id},
            {'$set': {
                'preference': preference,
                'preference_recorded_at': now,
                'updated_at': now
            }}
        )
        
        return Response({
            'id': str(object_id),
            'preference': preference,
            'preference_recorded_at': now.isoformat()
        })
    
    @action(detail=False, methods=['get'])
    def export_training_data(self, request):
        prompts = Prompt.objects.filter(preference__isnull=False).exclude(preference='TIE')
        training_data = []
        
        for prompt_obj in prompts:
            pair = prompt_obj.get_training_pair()
            if pair:
                training_data.append(pair)
        
        return Response({
            'count': len(training_data),
            'data': training_data
        })
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total = Prompt.objects.count()
        with_preference = Prompt.objects.filter(preference__isnull=False).count()
        preference_a = Prompt.objects.filter(preference='A').count()
        preference_b = Prompt.objects.filter(preference='B').count()
        ties = Prompt.objects.filter(preference='TIE').count()
        
        return Response({
            'total_prompts': total,
            'with_preference': with_preference,
            'without_preference': total - with_preference,
            'preference_a': preference_a,
            'preference_b': preference_b,
            'ties': ties,
            'training_pairs': preference_a + preference_b
        })
