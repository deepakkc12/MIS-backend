from datetime import datetime
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from ..utils.response import ResponseHandler
from ..services.Authentication import AuthUser,AuthCookieHandler
from ..utils.decorators import token_required

class Login(APIView):
    def post(self, request: Request) -> Response:
        """Handle user login requests."""
        username = request.data.get('username')
        password = request.data.get('password')

        print(username,password)

        if not username or not password:
            return ResponseHandler.bad_request("Username and password are required")

        auth_user, token, cookie_settings = AuthUser.authenticate(
            username=username,
            password=password
        )

        # employee_details = auth_user.get_employee()

        # if employee_details and not employee_details.IsActive:
        #     return ResponseHandler.forbidden('Employee Not Active')

        # kot_type = None
        # if employee_details and employee_details.KotTypeCode:
        #     kot_type_ins = KotType.find_by_id(employee_details.KotTypeCode)
        #     if kot_type_ins.IsActive:
        #         kot_type = kot_type_ins

        # branch = Branch.find_by_id(id=auth_user.branch_code)

        if auth_user:
            user_data = {
                "token":token,
                "code": auth_user.code,
                "privileges":auth_user.privileges,
                "username": auth_user.username,
                "isAdmin": auth_user.is_admin,
                "branchCode": auth_user.branch_code,
                # "branchName": branch.Name,
                # "branchPhone": branch.PhoneNo,

                # "employee":{
                #     'kotTypeCode':kot_type.Code if kot_type else None ,
                #     'kotTypeName':kot_type.Name if kot_type else None,
                #     'isActive':employee_details.IsActive,
                #     'code':employee_details.Code,
                # }if employee_details else None
            }

            response = ResponseHandler.success(data=user_data)

            return AuthCookieHandler.set_cookie(response=response,token=token)

        return ResponseHandler.unauthorized()



class Logout(APIView):
    def post(self, request: Request) -> Response:
        """Handle user logout requests."""
        try:
            AuthUser.logout(request=request)
            
            response = ResponseHandler.success("Logged out successfully")
            
            # Clear the auth token cookie
            response.delete_cookie('auth_token')
            
            return response
            
        except Exception as e:
            return ResponseHandler.internal_server_error(str(e))
        



class ChangePassword(APIView):
    def post(self, request: Request) -> Response:
        """Handle password change requests."""
        try:
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')
            
            if not old_password or not new_password:
                return ResponseHandler.bad_request("Old and new passwords are required")
            
            # Get current user from token
            current_user = AuthUser.connect(request)
            if not current_user:
                return ResponseHandler.unauthorized()
            
            # Attempt to change password
            success = AuthUser.change_password(
                user_code=current_user.code,
                old_password=old_password,
                new_password=new_password
            )
            
            if success:
                return ResponseHandler.success("Password changed successfully")
            else:
                return ResponseHandler.bad_request("Invalid old password")
            
        except Exception as e:
            return ResponseHandler.internal_server_error(str(e))


class ValidateToken(APIView):

    @token_required(admin_required=True)
    def get(self, request: Request) -> Response:
        """Validate the current user's token and return user data if valid."""
        try:
            current_user = AuthUser.connect(request)
            
            if current_user:
                user_data = {
                    "code": current_user.code,
                    "username": current_user.username,
                    "isAdmin": current_user.is_admin,
                    # "mobileNo": current_user.mobile_no,
                    "branchCode": current_user.branch_code,
                    # "loginCode": current_user.login_code
                }
                return ResponseHandler.success(data=user_data)
                
            return ResponseHandler.unauthorized()
            
        except Exception as e:
            return ResponseHandler.internal_server_error(str(e))
        

class GetLoginedBranchDetails(APIView):
    @token_required
    def get(self,request):
        auth_user = AuthUser.connect(request=request)

        branch_details = auth_user.get_branch_details()

        return ResponseHandler.success(data=branch_details)
