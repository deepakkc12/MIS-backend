from .response import *
import logging


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



from datetime import datetime
from typing import Optional

class DatabaseError(Exception):
    """Base exception for database errors"""
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.original_error = original_error
        self.timestamp = datetime.now()
        self.message = message

    def __str__(self):
        return f"{self.message} (at {self.timestamp})"



class TransactionError(DatabaseError):
    """Exception for transaction-related errors"""
    pass

class ConnectionError(DatabaseError):
    """Exception for connection-related errors"""
    pass


class AuthenticationError(Exception):
    """Exception raised for authentication-related errors."""
    
    def __init__(self, message="Authentication failed"):
        super().__init__(message)


class UnAuthorizedError(Exception):
    """Exception raised for authentication-related errors."""
    
    def __init__(self, message="Authentication failed"):
        super().__init__(message)

class PermissionDeniedError(Exception):
    """Exception raised for permission-related errors."""
    
    def __init__(self, message="Permission denied"):
        super().__init__(message)

class NotFoundError(Exception):
    """Exception raised for not found errors."""
    
    def __init__(self, message="Resource not found"):
        super().__init__(message)

class InternalServerError(Exception):
    """Exception raised for internal server errors."""
    
    def __init__(self, message="Internal server error occurred"):
        super().__init__(message)

class ValidationError(Exception):
    """Exception raised for validation errors."""
    
    def __init__(self, message="Validation error occurred"):
        super().__init__(message)




class ExceptionHandler:
    @staticmethod
    def handle_exception(exception):
        """Handles exceptions and returns a proper response."""
        if isinstance(exception, DatabaseError):
            return ResponseHandler.bad_request(errors=[str(exception)], message="Database error occurred.")
        elif isinstance(exception, AuthenticationError):
            return ResponseHandler.unauthorized(errors=[str(exception)], message="Authentication failed.")
        elif isinstance(exception, UnAuthorizedError):
            return ResponseHandler.unauthorized(errors=[str(exception)], message="Not Authenticated.")
        elif isinstance(exception, PermissionDeniedError):
            return ResponseHandler.forbidden(errors=[str(exception)], message="Permission denied.")
        elif isinstance(exception, NotFoundError):
            return ResponseHandler.not_found(errors=[str(exception)], message="Resource not found.")
        elif isinstance(exception, ValidationError):
            return ResponseHandler.bad_request(errors=[str(exception)], message="Validation error: Invalid or missing data.")
        else:
            print(ResponseHandler.internal_server_error())
            return ResponseHandler.internal_server_error(errors=[str(exception)])
        # print(response)
        # # Log the error before returning
        # logger.exception("Error occurred: %s", exception)
        # return response


    @staticmethod
    def propagate_error(exception):
        """Propagates the specific error by raising the corresponding custom exception."""
        if isinstance(exception, DatabaseError):
            raise DatabaseError(str(exception))
        elif isinstance(exception, AuthenticationError):
            raise AuthenticationError(str(exception))
        elif isinstance(exception, PermissionDeniedError):
            raise PermissionDeniedError(str(exception))
        elif isinstance(exception, NotFoundError):
            raise NotFoundError(str(exception))
        elif isinstance(exception, ValidationError):
            raise ValidationError(str(exception))
        elif isinstance(exception,ValueError):
            raise ValueError(str(exception))
        else:
            raise InternalServerError(f"An unexpected error occurred. {exception}")