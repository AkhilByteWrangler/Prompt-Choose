#!/usr/bin/env python
import os
import subprocess
import sys

# Get port from environment variable or use default
port = os.environ.get('PORT', '8000')

# Start gunicorn with the determined port
cmd = [
    'gunicorn',
    'backend.wsgi:application',
    '--bind', f'0.0.0.0:{port}',
    '--workers', '4'
]

print(f"Starting server on port {port}...")
sys.exit(subprocess.call(cmd))
