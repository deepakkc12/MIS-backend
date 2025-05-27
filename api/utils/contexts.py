from contextlib import contextmanager
from .exceptions import ExceptionHandler,ValidationError
from .response import ResponseHandler
from .validators import RequestValidator

@contextmanager
def handle_view_errors():
    try:
        yield  # This allows the block of code within the `with` statement to run.
    # except CustomException as e:
    #     response =ResponseHandler.bad_request() # Return response based on the exception
    #     return response  # Returning the response from the view context manager
    except Exception as e:
        return ResponseHandler.internal_server_error()  # Handle other exceptions
        print("response")
        print(response)
        return response  # Returning the response from the view context manager


@contextmanager
def propagate_errors():
    try:
        yield  # This allows the block of code within the `with` statement to run.
    # except CustomException as e:
    #     ExceptionHandler.propagate_error(e)  # Propagate the custom exception
    except Exception as e:
        ExceptionHandler.propagate_error(e)  # Propagate any other exception


@contextmanager
def validation(fields):
    """
    Context manager for validating fields and handling errors.
    
    Args:
        fields (dict): The fields to validate.
        
    Yields:
        dict: Validation result containing status and errors.
    """
    with propagate_errors():
        # Call the validation method and yield the result
        validation = RequestValidator.validate_all_fields(fields)
        if(validation['valid']):
            yield 
        else:
            raise ValidationError(validation['errors'])