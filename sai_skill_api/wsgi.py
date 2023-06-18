"""
WSGI config for sai_skill_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sai_skill_api.settings')
sys.path.append('/home/saiuser/sai_skill_api')

application = get_wsgi_application()
