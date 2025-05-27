import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
# The WSGI application callable for the Django project.
# This is used by WSGI servers to forward requests to the Django application.