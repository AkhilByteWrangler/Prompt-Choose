import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
application = get_wsgi_application()

# Log runtime environment info (only when workers start, not during build)
api_key = os.environ.get('OPENAI_API_KEY', '')
if api_key:
    print(f"✓ Runtime: OpenAI API Key loaded (starts with: {api_key[:15]}...)", file=sys.stderr)
else:
    print("⚠ Runtime: OPENAI_API_KEY is not set!", file=sys.stderr)
