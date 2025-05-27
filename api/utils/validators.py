# your_app/validators.py

from datetime import datetime
from django.http import HttpRequest


class RequestValidator:
    """
    A class that provides validation methods for different types of fields based on their name prefixes.
    The first five characters of the field name determine the validation type.
    """
    validation_status = True
    validation_errors = {}

    @staticmethod
    def validate_required_text(value, field_name):
        """Validates that the given field is a non-empty text."""
        if not value or not isinstance(value, str) or not value.strip():
            error_message = f"{field_name} must be a non-empty text."
            print(f"Validation Error: {error_message}")
            RequestValidator.validation_errors[field_name] = error_message
            RequestValidator.validation_status = False
            return False
        return True

    @staticmethod
    def validate_optional_text(value, field_name):
        """Validates that the given field is either empty or a valid text."""
        if value and not isinstance(value, str):
            error_message = f"{field_name} must be a text if provided."
            print(f"Validation Error: {error_message}")
            RequestValidator.validation_errors[field_name] = error_message
            RequestValidator.validation_status = False
            return False
        return True

    @staticmethod
    def validate_required_numeric(value, field_name):
        """Validates that the given field is a non-empty numeric value."""
        if value:
    # Check if value is not an instance of `int` or `float`
            if not isinstance(value, (int, float)):
                try:
                    # Try converting the value to float
                    value = float(value)
                except ValueError:
                    # If conversion fails, set the error message and return False
                    error_message = f"{field_name} must be a numeric value."
                    print(f"Validation Error: {error_message}")
                    RequestValidator.validation_errors[field_name] = error_message
                    RequestValidator.validation_status = False
                    return False
            # If no issues, return True
            return True
            

    @staticmethod
    def validate_optional_numeric(value, field_name):
        """Validates that the given field is either empty or a numeric value."""
        if value:
            return RequestValidator.validate_required_numeric(value, field_name)
        return True

    @staticmethod
    def validate_required_date(value, field_name, date_format="%Y-%m-%d"):
        """Validates that the given field is a non-empty date value in the specified format."""
        if not value:
            error_message = f"{field_name} must be a non-empty date."
            print(f"Validation Error: {error_message}")
            RequestValidator.validation_errors[field_name] = error_message
            RequestValidator.validation_status = False
            return False

        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            error_message = f"{field_name} must be a valid date in the format {date_format}."
            print(f"Validation Error: {error_message}")
            RequestValidator.validation_errors[field_name] = error_message
            RequestValidator.validation_status = False
            return False

    @staticmethod
    def validate_optional_date(value, field_name, date_format="%Y-%m-%d"):
        """Validates that the given field is either empty or a valid date value in the specified format."""
        if value:
            return RequestValidator.validate_required_date(value, field_name, date_format)
        return True
    @staticmethod
    def validate_list(value, field_name):
        """Validates that the given field is a non-empty list."""
        if not isinstance(value, list) :  # Check if it's a list and non-empty
            error_message = f"{field_name} must be a non-empty list."
            print(f"Validation Error: {value}")
            RequestValidator.validation_errors[field_name] = error_message
            RequestValidator.validation_status = False
            return False
        return True

    @staticmethod
    def validate_dict(value, field_name):
        """Validates that the given field is a dictionary."""
        if not value or not isinstance(value, dict):
            error_message = f"{field_name} must be a dictionary."
            print(f"Validation Error: {error_message}")
            RequestValidator.validation_errors[field_name] = error_message
            RequestValidator.validation_status = False
            return False
        return True

    @staticmethod
    def validate_field_by_prefix(field_name, value):
        """
        Determines the validation method based on the field's prefix and validates the value.
        
        ]Args:
            field_name (str): The name of the field to validate.
            value: The value of the field to validate.
        """
        # Define a shorter prefix extraction based on your new naming convention
        prefix = field_name.split('_')[0].upper()
        
        # Check and validate based on prefix type
        if prefix == "TXT":
            return RequestValidator.validate_required_text(value, field_name)
        elif prefix == "TXTO":
            return RequestValidator.validate_optional_text(value, field_name)
        elif prefix == "TXTN":
            return RequestValidator.validate_required_numeric(value, field_name)
        elif prefix == "TXTNO":
            return RequestValidator.validate_optional_numeric(value, field_name)
        elif prefix == "DT":
            return RequestValidator.validate_required_date(value, field_name)
        elif prefix == "DTO":
            return RequestValidator.validate_optional_date(value, field_name)
        elif prefix == "LST":
            return RequestValidator.validate_list(value, field_name)
        elif prefix == "DICT":
            return RequestValidator.validate_dict(value, field_name)
        else:
            error_message = f"Unknown prefix '{prefix}' in field name '{field_name}'."
            print(f"Validation Error: {error_message}")
            RequestValidator.validation_errors[field_name] = error_message
            RequestValidator.validation_status = False
            return False

    @staticmethod
    def validate_all_fields(request_data: dict) -> dict:
        """
        Validates all fields in the given request data based on their prefixes.

        Args:
            request_data (dict): The data dictionary to validate.

        Returns:
            dict: A dictionary with validation status and errors.
                  {"status": True/False, "errors": {"field_name": "error message", ...}}
        """
        RequestValidator.validation_status = True  # Reset validation status
        RequestValidator.validation_errors = {}  # Reset error messages


        for field_name, value in request_data.items():
            RequestValidator.validate_field_by_prefix(field_name, value)

        return {
            "valid": RequestValidator.validation_status,
            "errors": RequestValidator.validation_errors
        }
    @staticmethod
    def validate_request_fields(request:HttpRequest, fields:list):
        """
        Validates the fields from the request against the expected fields.

        Args:
            request: The HTTP request object containing the data.
            fields (list): A list of expected fields to validate.

        Returns:
            dict: A dictionary with validation status and errors.
                  {"status": True/False, "errors": {"field_name": "error message", ...}}
        """
        RequestValidator.validation_status = True  # Reset validation status
        RequestValidator.validation_errors = {}  # Reset error messages

        # Extracting data from the request
        extracted_data = {field: request.data.get(field) for field in fields}

        # Validate each field based on its prefix
        for field_name, value in extracted_data.items():
            RequestValidator.validate_field_by_prefix(field_name, value)

        return {
            "valid": RequestValidator.validation_status,
            "errors": RequestValidator.validation_errors
        }