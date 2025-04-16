# run_daphne.py
import os
import sys
import django
from daphne.server import Server
from daphne.endpoints import build_endpoint_description_strings

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Setup Django
django.setup()

# Import ASGI app AFTER setting up Django
from core.asgi import application

# Define host and port
host = "127.0.0.1"
port = 8000

# Prepare Daphne endpoints
endpoints = build_endpoint_description_strings(host=host, port=port)

# Start Daphne server
Server(
    application=application,
    endpoints=endpoints,
    signal_handlers=False
).run()
