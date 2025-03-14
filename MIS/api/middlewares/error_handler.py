from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework import status
import logging
from ..utils.exceptions import ExceptionHandler

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        print("Processing view:", view_func.__name__)
        try:
            # Continue to process the view function
            response = view_func(request, *view_args, **view_kwargs)
            return response
        except Exception as e:
            logger.error(f"Unexpected exception occurred: {e}")
            # Use DRF's exception handler
            response = exception_handler(e, context={'request': request})
            if response is None:
                # If DRF couldn't handle it, return a generic error response
                return ExceptionHandler.handle_exception(e)
            return response