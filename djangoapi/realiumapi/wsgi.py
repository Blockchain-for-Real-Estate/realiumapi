import os
import sys

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
# sys.path.append('/home/ubuntu/realiumapi/djangoapi/realiumapi')
sys.path.append('/home/ubuntu/env')
# os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/projects/realiumapi/djangoapi/realiumapi/egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realiumapi.djangoapi.realiumapi.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
