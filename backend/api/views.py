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
import logging

logger = logging.getLogger(__name__)


class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        logger.info(f"Looking up prompt with pk: {pk}, type: {type(pk)}")
        
        try:
            # Convert string pk to ObjectId for MongoDB
            if isinstance(pk, str):
                pk = ObjectId(pk)
            
            obj = Prompt.objects.get(_id=pk)
            logger.info(f"Found prompt with pk: {obj.pk}")
            return obj
        except Prompt.DoesNotExist:
            logger.error(f"Prompt not found with pk: {pk}")
            try:
                existing_ids = list(Prompt.objects.values_list('pk', flat=True)[:5])
                logger.error(f"Existing IDs in database: {existing_ids}")
            except:
                pass
            from rest_framework.exceptions import NotFound
            raise NotFound(f'Prompt not found with id: {pk}')
        except Exception as e:
            logger.error(f"Error during lookup: {e}")
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
            logger.error(f"Configuration error: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error generating responses: {error_msg}", exc_info=True)
            
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
        
        prompt_obj = Prompt.objects.create(
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
        
        return Response({
            'id': str(prompt_obj.pk),
            'prompt': prompt_obj.prompt_text,
            'response_a': prompt_obj.response_a,
            'response_b': prompt_obj.response_b,
            'model_name': prompt_obj.model_name,
            'temperature': prompt_obj.temperature,
            'temperature_a': prompt_obj.temperature_a,
            'temperature_b': prompt_obj.temperature_b,
            'created_at': prompt_obj.created_at.isoformat()
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_path='record-preference')
    def record_preference(self, request, pk=None):
        prompt_obj = self.get_object()
        serializer = RecordPreferenceSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        preference = serializer.validated_data['preference']
        prompt_obj.preference = preference
        prompt_obj.preference_recorded_at = timezone.now()
        prompt_obj.save()
        
        return Response({
            'id': str(prompt_obj.pk),
            'preference': prompt_obj.preference,
            'preference_recorded_at': prompt_obj.preference_recorded_at.isoformat() if prompt_obj.preference_recorded_at else None
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
