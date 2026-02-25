from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.utils import timezone
from django.conf import settings
from bson import ObjectId
from .models import Prompt
from .serializers import (
    PromptSerializer,
    GenerateResponsesSerializer,
    RecordPreferenceSerializer,
    TrainingDataSerializer,
)
from .llm_service import generate_two_responses
import pymongo

_mongo_client = None

def _get_collection():
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = pymongo.MongoClient(settings.MONGODB_URI)
    return _mongo_client[settings.MONGODB_NAME]['api_prompt']


class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            if isinstance(pk, str):
                pk = ObjectId(pk)
            return Prompt.objects.get(_id=pk)
        except (Prompt.DoesNotExist, Exception) as e:
            raise NotFound(str(e))
    
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
            if 'authentication' in error_msg.lower() or 'api key' in error_msg.lower() or 'unauthorized' in error_msg.lower():
                error_response = 'Invalid API key.'
            elif 'quota' in error_msg.lower() or 'billing' in error_msg.lower():
                error_response = 'OpenAI quota exceeded.'
            elif 'rate limit' in error_msg.lower():
                error_response = 'Rate limit exceeded. Try again in a moment.'
            elif 'model' in error_msg.lower():
                error_response = f'{model_name} may not be available.'
            else:
                error_response = error_msg[:100]
            return Response({'error': error_response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        now = timezone.now()
        collection = _get_collection()
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
        serializer = RecordPreferenceSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        preference = serializer.validated_data['preference']
        now = timezone.now()

        try:
            object_id = ObjectId(pk) if isinstance(pk, str) else pk
        except Exception:
            raise NotFound(f'Invalid ObjectId format: {pk}')
        
        collection = _get_collection()
        
        result = collection.update_one(
            {'_id': object_id},
            {'$set': {
                'preference': preference,
                'preference_recorded_at': now,
                'updated_at': now
            }}
        )
        
        if result.matched_count == 0:
            raise NotFound(f'Prompt not found with id: {pk}')
        
        return Response({
            'id': str(object_id),
            'preference': preference,
            'preference_recorded_at': now.isoformat()
        })
    
    @action(detail=False, methods=['get'], url_path='export-training-data')
    def export_training_data(self, request):
        collection = _get_collection()
        docs = collection.find({'preference': {'$in': ['A', 'B']}})
        training_data = []
        for doc in docs:
            chosen = doc['response_a'] if doc['preference'] == 'A' else doc['response_b']
            rejected = doc['response_b'] if doc['preference'] == 'A' else doc['response_a']
            training_data.append({
                'prompt': doc['prompt_text'],
                'chosen': chosen,
                'rejected': rejected,
                'metadata': {
                    'model': doc.get('model_name'),
                    'temperature': doc.get('temperature'),
                    'temperature_a': doc.get('temperature_a'),
                    'temperature_b': doc.get('temperature_b'),
                    'created_at': doc['created_at'].isoformat() if doc.get('created_at') else None,
                    'preference_recorded_at': doc['preference_recorded_at'].isoformat() if doc.get('preference_recorded_at') else None,
                }
            })
        return Response({'count': len(training_data), 'data': training_data})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        collection = _get_collection()
        total = collection.count_documents({})
        preference_a = collection.count_documents({'preference': 'A'})
        preference_b = collection.count_documents({'preference': 'B'})
        ties = collection.count_documents({'preference': 'TIE'})
        with_preference = preference_a + preference_b + ties
        return Response({
            'total_prompts': total,
            'with_preference': with_preference,
            'without_preference': total - with_preference,
            'preference_a': preference_a,
            'preference_b': preference_b,
            'ties': ties,
            'training_pairs': preference_a + preference_b,
        })
