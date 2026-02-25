from djongo import models


class Prompt(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    prompt_text = models.TextField()
    response_a = models.TextField()
    response_b = models.TextField()
    
    model_name = models.CharField(max_length=100, default='gpt-3.5-turbo')
    temperature = models.FloatField(default=0.7)
    
    temperature_a = models.FloatField(default=0.7)
    max_tokens_a = models.IntegerField(default=500)
    top_p_a = models.FloatField(default=1.0)
    frequency_penalty_a = models.FloatField(default=0.0)
    presence_penalty_a = models.FloatField(default=0.0)
    
    temperature_b = models.FloatField(default=0.9)
    max_tokens_b = models.IntegerField(default=500)
    top_p_b = models.FloatField(default=1.0)
    frequency_penalty_b = models.FloatField(default=0.0)
    presence_penalty_b = models.FloatField(default=0.0)
    
    response_a_generated_at = models.DateTimeField(null=True, blank=True)
    response_b_generated_at = models.DateTimeField(null=True, blank=True)
    
    preference = models.CharField(
        max_length=10,
        choices=[('A', 'Response A'), ('B', 'Response B'), ('TIE', 'Tie')],
        null=True,
        blank=True
    )
    preference_recorded_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prompt {self.pk}: {self.prompt_text[:50]}..."
    
    def get_training_pair(self):
        if not self.preference or self.preference == 'TIE':
            return None
        
        chosen = self.response_a if self.preference == 'A' else self.response_b
        rejected = self.response_b if self.preference == 'A' else self.response_a
        
        return {
            'prompt': self.prompt_text,
            'chosen': chosen,
            'rejected': rejected,
            'metadata': {
                'model': self.model_name,
                'temperature': self.temperature,
                'temperature_a': self.temperature_a,
                'temperature_b': self.temperature_b,
                'created_at': self.created_at.isoformat(),
                'preference_recorded_at': self.preference_recorded_at.isoformat() if self.preference_recorded_at else None,
            }
        }
