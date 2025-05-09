from enum import Enum
import logging
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from typing import Dict, Optional, Tuple
from django.http import HttpRequest
from ..Core import db
from ..models.Models import Users
from ..utils.exceptions import AuthenticationError, InternalServerError
from ..utils.contexts import propagate_errors
import secrets
from ..utils.Encryptor import AESCipher
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class AuthCookieHandler:

    """Handles authentication cookie operations."""
    
    COOKIE_NAME = 'auth_token'
    
    @classmethod
    def set_cookie(cls, response: HttpResponse, token: str) -> HttpResponse:
        """
        Set the authentication cookie with proper settings.
        """
        cookie_settings = {
            'max_age': 24 * 60 * 60,  # 24 hours in seconds
            'httponly': True,  # Prevents JavaScript access
            'secure': not settings.DEBUG,  # True in production
            'samesite': 'Lax',  # Protects against CSRF
            'path': '/',  # Cookie available for all paths
            'domain': None  # Use current domain
        }

        response.set_cookie(
            cls.COOKIE_NAME,
            token,
            **cookie_settings
        )
        
        return response


class AuthUser:
    encrypter = AESCipher()

    def __init__(self, code: int, username: str, is_admin: bool, 
                 branch_code: int, token: str = None,login_code:str = None) -> None:
        
        self.code = code
        self.logi_code = login_code
        self.username = username
        self.privileges = self.get_privileges()
        self.branch_code = branch_code
        self.token = token
        self.is_active = True

    def get_privileges(self):

        query = """Select menuOptionCode FROM userMenuOption WITH (NOLOCK) wHERE userCode = ?"""
        param = [self.code]
        result = db.get_data(query=query,data=param)

        if result:
            return [row['menuOptionCode'] for row in result]
        return []
    

    
    def get_branch_details(self):
        query = """select Code,Name,DOT,Remark,Address,PhoneNo from Branches Where Code = ?"""
        param = [self.branch_code]

        result = db.get_data(query=query,data=param)

        result = result[0] if result else None

        return  result

    
    def has_privilege(self,privilege):
        return privilege in self.privileges

    @staticmethod
    def _generate_token() -> str:
        """Generate a secure random token"""
        return secrets.token_urlsafe(32)

    @classmethod
    def _hash_password(cls,password: str) -> str:

        return cls.encrypter.encrypt(password)    
    
    @classmethod
    def verify_pin(cls,pin)->bool:
        query = """SELECT CODE FROM USERS WITH (NOLOCK) WHERE ENCPIN = ?"""
        hashed_pin = cls._hash_password(password=pin)
        result = db.get_data(query=query,data=[hashed_pin])

        if result:
            return True
        else:
            return False

    @classmethod
    def authenticate(cls, username: str, password: str) -> Optional[Tuple['AuthUser', str, Dict]]:
        """
        Authenticate a user with username and password.
        Returns a tuple of (User instance, token, cookie_settings) on success.
        """
        with propagate_errors():
            if not username or not password:
                logger.error("Username or password is empty.")
                raise ValueError("Username or password is empty.")
            
            hashed_pin = cls._hash_password(password=password)

            result = Users.filter(Username=username,encPin=hashed_pin,IsActive=1,)

            if not result:
                logger.warning("Authentication failed for user: %s", username)
                raise AuthenticationError(message="Authentication failed")

            user_data = result[0]
            
            # Generate new token
            token = cls._generate_token()
            print("user.............................................1")

            
            # Update user's token in database
            update_query = """
                UPDATE Users
                SET Token = ?
                WHERE Code = ?
            """
            
            # token_expiry = datetime.utcnow() + timedelta(hours=48)
            
            db.update(update_query, [token, user_data.Code])

            # Create AuthUser instance
            user = cls(
                code=user_data.Code,
                username=user_data.Username,
                is_admin=user_data.IsAdmin,
                branch_code=user_data.BranchCode,
                login_code = user_data.LoginCode,
                token=token
            )

            cookie_settings = {
                'max_age': 17280000,  # 48 hours in seconds
                'path': '/',
                'secure': True,
                'httponly': True,
                'samesite': 'Lax'
            }

            logger.info("Authentication successful for user: %s", username)
            return (user, token, cookie_settings)


        
    @staticmethod
    def _get_token_from_request(request: HttpRequest) -> Optional[str]:
        """
        Try multiple methods to get the authentication token.
        """
        # 1. Try cookie
        token = request.COOKIES.get(AuthCookieHandler.COOKIE_NAME)
        if token:
            return token
            
        # 2. Try Authorization header
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header.replace('Bearer ', '')
            
        # 3. Try query parameter
        return request.GET.get('token')


    @classmethod
    def logout(cls,request: HttpRequest) -> None:
        """Log out the current user by invalidating their token."""
        with propagate_errors():
            token = cls._get_token_from_request(request=request)
            if token:
                update_query = """
                    UPDATE Users
                    SET Token = NULL
                    WHERE Token = ?
                """
                db.update(update_query, [token])
                logger.info("User logged out successfully")

    @classmethod
    def connect(cls, request: HttpRequest) -> Optional['AuthUser']:
        """Retrieve the user instance from token if available."""

        print("All cookies:", request.COOKIES)
        # print("Headers:", request.headers)
        
        # Try multiple methods to get the token
        token = cls._get_token_from_request(request)
        
        if not token:
            print("No token found in request")
            return None

        query = """
            SELECT Code, Username, IsAdmin, BranchCode, LoginCode,  DOT
            FROM Users WITH (NOLOCK)
            WHERE Token = ? AND IsActive = 1
        """
        
        # current_time = datetime.utcnow()
        
        result = db.get_data(query, [token])

        if not result:
            return None

        user_data = result[0]
        
        return cls(
            code=user_data['Code'],
            username=user_data['Username'],
            is_admin=user_data['IsAdmin'],
            branch_code=user_data['BranchCode'],
            login_code=user_data['LoginCode'],
            token=token
        )
    

    def get_price_code(self):
        querry = """SELECT k.PriceCode
                    FROM Users u
                    JOIN Employee e ON u.Code = e.UserCode
                    JOIN KotType k ON e.KotTypeCode = k.Code
                    WHERE u.Code = ?; """
        
        result = db.get_data(query=querry,data=[self.code])
        price_code = result[0]['PriceCode'] if result else None

        if price_code :
            if price_code  > 3:
                return 3
            return price_code
        return 1


    @staticmethod
    def generate_enc_pin(pin):
        cipher = AESCipher()

        enc_pin = cipher.encrypt(pin)

        return enc_pin


    @staticmethod
    def change_password(user_code: int, old_password: str, new_password: str) -> bool:
        """Change user's password."""
        with propagate_errors():
            # Hash passwords
            old_hash = old_password
            new_hash = new_password

            enc_pin = AuthUser.generate_enc_pin(pin=new_hash)
            
            # Verify old password and update to new one
            query = """
                UPDATE Users
                SET Pswd = ?,encPin = ?
                WHERE Code = ? AND Pswd = ?
            """
            
            result = db.update(query, [new_hash,enc_pin, user_code, old_hash])
            
            if result:
                logger.info(f"Password changed successfully for user code: {user_code}")
                return True
            else:
                logger.warning(f"Password change failed for user code: {user_code}")
                return False
