import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
sys.path.append('/home/ubuntu/realiumapi/djangoapi/realiumapi')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realiumapi.settings')

application = get_wsgi_application()
