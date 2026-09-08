"""
WSGI config for tcet_chatbot project.
Standard Django file - lets a real web server run this project.
Not important for the viva, just required boilerplate.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tcet_chatbot.settings')

application = get_wsgi_application()
