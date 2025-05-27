from django.http import HttpRequest
from ..services.Authentication import AuthUser
from django.conf import settings


class AuthenticationMiddleware:
    """Middleware to process authentication tokens and attach user to request."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        """Process each request through the middleware."""
        
        # Skip authentication for excluded paths
        if self._is_excluded_path(request.path):
            return self.get_response(request)

        # Try to get user from token
        # request.authuser = AuthUser.connect(request)
        # print(request.user)
        
        return self.get_response(request)

    def _is_excluded_path(self, path: str) -> bool:
        """Check if the path should be excluded from authentication."""
        excluded_paths = getattr(settings, 'AUTH_EXCLUDED_PATHS', [
            '/api/login/',
            '/api/register/',
            '/api/forgot-password/',
        ])
        
        return any(path.startswith(excluded_path) for excluded_path in excluded_paths)