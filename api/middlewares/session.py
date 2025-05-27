from ..services.Authentication import UserSessionManager

class SessionMiddleware:
       def __init__(self, get_response):
           self.get_response = get_response

       def __call__(self, request):
           user = UserSessionManager.get_session_data(request)
           request.user = user  # Attach the user to the request
           response = self.get_response(request)
           return response