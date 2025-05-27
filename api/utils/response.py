from django.http import JsonResponse
from rest_framework import status

class ResponseHandler:

    @staticmethod
    def success(message: str = "Success", data=None, status_code=status.HTTP_200_OK):
        response = {
            "success": True,
            "message": message,
            "data": data,
        }
        return JsonResponse(response, status=status_code)

    @staticmethod
    def created(message: str = "Resource created successfully", data=None):
        response = {
            "success": True,
            "message": message,
            "data": data,
        }
        
        return JsonResponse(response, status=status.HTTP_201_CREATED)

    @staticmethod
    def no_content(message: str = "No content"):
        response = {
            "success": True,
            "message": message,
        }
        return JsonResponse(response, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def bad_request(message: str = "Invalid request", errors=None):
        print("bad request")
        response = {
            "success": False,
            "message": message,
            "errors": errors,
        }
        return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def unauthorized(message: str = "Unauthorized access", errors=None):
        response = {
            "success": False,
            "message": message,
            "errors": errors,
        }
        return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def forbidden(message: str = "Forbidden", errors=None):
        response = {
            "success": False,
            "message": message,
            "errors": errors,
        }
        return JsonResponse(response, status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def not_found(message: str = "Resource not found", errors=None):
        response = {
            "success": False,
            "message": message,
            "errors": errors,
        }
        return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def conflict(message: str = "Conflict with current state", errors=None):
        response = {
            "success": False,
            "message": message,
            "errors": errors,
        }
        return JsonResponse(response, status=status.HTTP_409_CONFLICT)

    @staticmethod
    def unprocessable_entity(message: str = "Unprocessable entity", errors=None):
        response = {
            "success": False,
            "message": message,
            "errors": errors,
        }
        return JsonResponse(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @staticmethod
    def internal_server_error(message: str = "Internal server error", errors=None):
        response = {
            "success": False,
            "message": message,
            "errors": errors,
        }
        return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def service_unavailable(message: str = "Service unavailable", errors=None):
        response = {
            "success": False,
            "message": message,
            "errors": errors,
        }
        return JsonResponse(response, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    

    @staticmethod
    def success_with_cookie(message: str = "Success", data=None, cookies=None, status_code=status.HTTP_200_OK):
        """
        This method allows setting cookies in the response.
        :param message: The message for the response
        :param data: The data to include in the response
        :param cookies: A dictionary of cookies to set (e.g., {'cookie_name': 'cookie_value'})
        :param status_code: The HTTP status code for the response
        """
        response = JsonResponse({
            "success": True,
            "message": message,
            "data": data,
        }, status=status_code)

        if cookies:
            for cookie_name, cookie_value in cookies.items():
                response.set_cookie(cookie_name, cookie_value)

        return response