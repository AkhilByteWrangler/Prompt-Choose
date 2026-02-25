from django.contrib import admin
from .models import Prompt


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ['prompt_text_short', 'preference', 'created_at']
    list_filter = ['preference', 'created_at', 'model_name']
    search_fields = ['prompt_text', 'response_a', 'response_b']
    readonly_fields = ['created_at', 'updated_at', 'response_a_generated_at', 'response_b_generated_at']
    
    def prompt_text_short(self, obj):
        return obj.prompt_text[:50] + '...' if len(obj.prompt_text) > 50 else obj.prompt_text
    prompt_text_short.short_description = 'Prompt'
