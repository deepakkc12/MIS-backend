from typing import Callable, List, Type
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps
from ..services.Authentication import AuthUser
from .exceptions import PermissionDeniedError
from rest_framework.views import APIView
from django.http import HttpRequest
from .response import ResponseHandler

def token_required(
    view_func: Callable = None, 
    admin_required: bool = False, 
    required_privileges: List[str] = None
) -> Callable:
    """
    Decorator to enforce token authentication, admin access, and privilege checks for views.
    
    Args:
        view_func: The view function to decorate
        admin_required: If True, requires the user to be an admin
        required_privileges: A list of privileges the user must have to access the view
    
    Usage:
        @token_required
        def my_view(request):
            # Regular user access
            pass
            
        @token_required(admin_required=True)
        def admin_view(request):
            # Admin only access
            pass

        @token_required(required_privileges=["KOT", "C-CNTR"])
        def privilege_view(request):
            # Access restricted to users with "KOT" or "C-CNTR" privileges
            pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(view_instance: Type[APIView], request: HttpRequest, *args, **kwargs):
            # Check if user is authenticated
            if not hasattr(request, 'authuser') or request.authuser is None:
                return ResponseHandler.unauthorized("Token Expired, Authentication required")
            
            # Check admin requirement
            if admin_required and not request.authuser.is_admin:
                return ResponseHandler.forbidden("Admin access required")

            # Check for required privileges
            if required_privileges:
                user_privileges = request.authuser.privileges
                if not any(privilege in user_privileges for privilege in required_privileges):
                    return ResponseHandler.forbidden("Insufficient privileges to access this resource")
            
            return view_func(view_instance, request, *args, **kwargs)
        return wrapped_view

    # Handle both @token_required and @token_required() syntax
    if view_func is None:
        return decorator
    return decorator(view_func)