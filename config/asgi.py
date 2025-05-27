import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
# import POS.api.routing  # Adjust if you have channels routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
})
