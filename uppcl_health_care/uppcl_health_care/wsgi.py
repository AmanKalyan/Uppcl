import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uppcl_health_care.settings')
application = get_wsgi_application()
