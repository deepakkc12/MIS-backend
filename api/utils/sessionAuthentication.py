import os
import logging
from typing import Dict, Optional, Tuple
from django.db import connection
from ..utils.db import db
# from ..utils.session import SessionManager
from ..utils.exceptions import AuthenticationError, InternalServerError
from ..utils.contexts import propagate_errors
from ..utils.helpers import get_current_date

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data Class to Hold User-Specific Information
class User:
    def __init__(self, _name: str, _id: str, _isAdmin: bool, _uid: str) -> None:
        self._name = _name
        self._id = _id
        self._isAdmin = _isAdmin
        self._uid = _uid

    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id

    @classmethod
    def authenticate(cls, request, username: str, password: str) -> Optional[Tuple['User', str, Dict]]:
        with propagate_errors():
            if not username or not password:
                logger.error("Username or password is empty.")
                return {'error': 'Username and password are required.'}
            
            query = """SELECT * FROM Login WHERE UID = %s AND Password = %s;"""
            user = db.get_data(query, [username, password])
            user = user[0] if user else None

            if user:
                # Get both session_id and cookie settings
                session_id, cookie_settings = UserSessionManager.set_session_data(
                    request, 
                    user['Name'], 
                    user['ID'], 
                    is_admin=user['isAdmin'], 
                    uid=user['UID']
                )
                logger.info("Authentication successful for user: %s", username)
                return (
                    cls(_name=user['Name'], _id=user['ID'], _uid=user['UID'], _isAdmin=user['isAdmin']),
                    session_id,
                    cookie_settings
                )
            else:
                logger.warning("Authentication failed for user: %s", username)
                raise AuthenticationError(message="Authentication failed")

    @staticmethod
    def logout(request) -> None:
        with propagate_errors():
            UserSessionManager.clear_session_data(request)
        
    @staticmethod
    def connect(request) -> Optional['User']:
        user_instance = UserSessionManager.get_session_data(request)
        if user_instance:
            return user_instance
        return None

import os
import logging
from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta
import uuid
import json
from ..utils.db import db
from ..utils.exceptions import AuthenticationError, InternalServerError
from ..utils.contexts import propagate_errors
from ..utils.helpers import get_current_date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import json
import uuid
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from typing import Dict, Tuple, Optional

class UserSessionManager:

    COOKIE_NAME = 'session_id'
    SESSION_DURATION = timedelta(hours=48)
    
    # Generate a key for encryption (this should be done once and securely stored)
    # For production, securely generate and store the key
    SECRET_KEY = Fernet.generate_key()
    cipher_suite = Fernet(SECRET_KEY)

    @staticmethod
    def _generate_session_id() -> str:
        return str(uuid.uuid4())
    
    @staticmethod
    def _get_cookie_settings(expires_at: datetime) -> Dict:
        return {
            'max_age': 86400,
            'path': '/',
            'secure': False,  # Enable for HTTPS
            'httponly': True,
            'samesite': 'Lax'
        }
    
    @staticmethod
    def close_current_session(uid):
        existing_sessions_query = """
            SELECT session_id, user_data 
            FROM sessions 
            WHERE is_active = 1;
        """
        existing_sessions = db.get_data(existing_sessions_query)

        # Loop through existing sessions and check for matching uid
        for session in existing_sessions:
            decrypted_user_data = UserSessionManager.cipher_suite.decrypt(session['user_data']).decode()
            existing_uid = json.loads(decrypted_user_data)['_uid']
            
            if existing_uid == uid:
                # Invalidate this session
                update_query = """
                    UPDATE sessions 
                    SET is_active = 0 
                    WHERE session_id = %s;
                """
                db.update(update_query, [session['session_id']])

    @staticmethod
    def set_session_data(request, username: str, user_id: str, is_admin: bool, uid: str) -> Tuple[str, Dict]:
        """
        Create a new session and return both session_id and cookie settings.
        Returns: Tuple of (session_id, cookie_settings)
        """
        try:
            session_id = UserSessionManager._generate_session_id()
            current_time = datetime.utcnow()
            expires_at = current_time + UserSessionManager.SESSION_DURATION
            
            # Prepare user data for encryption
            user_data = json.dumps({
                "_name": username,
                "_id": user_id,
                "_isAdmin": is_admin,
                "_uid": uid
            })
            
            # Encrypt the user data
            encrypted_user_data = UserSessionManager.cipher_suite.encrypt(user_data.encode())

            # Invalidate existing sessions
            UserSessionManager.close_current_session(uid=uid)
            # db.update(invalidate_query, [uid])
            
            # Insert new session with encrypted data
            insert_query = """
                INSERT INTO sessions (session_id, user_data, expires_at, is_active)
                VALUES (%s, %s, %s, 1);
            """
            db.post_data(insert_query, [session_id, encrypted_user_data, expires_at])
            
            # Return both session_id and cookie settings
            cookie_settings = UserSessionManager._get_cookie_settings(expires_at)
            return session_id, cookie_settings
            
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            raise InternalServerError("Failed to create session")

    @staticmethod
    def get_session_data(request) -> Optional['User']:
        try:
            session_id = request.COOKIES.get(UserSessionManager.COOKIE_NAME)
            
            if not session_id:
                logger.debug("No session ID found in request")
                return None
            
            query = """
                SELECT user_data, expires_at 
                FROM sessions 
                WHERE session_id = %s 
                    AND is_active = 1 
                    AND expires_at > GETDATE();
            """
            result = db.get_data(query, [session_id])
            
            if not result:
                logger.debug("No valid session found")
                return None
            
            # Refresh session expiration if it's close to expiring
            session_data = result[0]
            expires_at = session_data['expires_at']
            if datetime.utcnow() + timedelta(hours=1) > expires_at:
                new_expires = datetime.utcnow() + UserSessionManager.SESSION_DURATION
                refresh_query = """
                    UPDATE sessions 
                    SET expires_at = %s 
                    WHERE session_id = %s;
                """
                db.update(refresh_query, [new_expires, session_id])
            
            # Decrypt the user data
            decrypted_user_data = UserSessionManager.cipher_suite.decrypt(session_data['user_data']).decode()
            user_data = json.loads(decrypted_user_data)
            return User(**user_data)
            
        except Exception as e:
            logger.error(f"Error retrieving session: {e}")
            return None

    @staticmethod
    def clear_session_data(request) -> None:
        try:
            session_id = request.COOKIES.get(UserSessionManager.COOKIE_NAME)
            if session_id:
                query = """
                    UPDATE sessions 
                    SET is_active = 0 
                    WHERE session_id = %s;
                """
                db.update(query, [session_id])
                logger.info(f"Session {session_id} invalidated")
        except Exception as e:
            logger.error(f"Error clearing session: {e}")
            raise InternalServerError("Failed to clear session")