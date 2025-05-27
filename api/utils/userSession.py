# import os
# import logging
# from typing import Optional, Dict, Tuple
# from datetime import datetime, timedelta
# import uuid
# import json

# from ..utils.db import db
# from ..utils.exceptions import AuthenticationError, InternalServerError
# from ..utils.contexts import propagate_errors
# from ..utils.helpers import get_current_date

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class UserSessionManager:
#     COOKIE_NAME = 'session_id'
#     SESSION_DURATION = timedelta(hours=48)

#     @staticmethod
#     def _generate_session_id() -> str:
#         return str(uuid.uuid4())
    
#     @staticmethod
#     def _get_cookie_settings(expires_at: datetime) -> Dict:
#         return {
#             # 'expires': expires_at,
#             'max_age':86400,
#             'path': '/',
#             'secure': False,  # Enable for HTTPS
#             'httponly': True,
#             'samesite': 'Lax'
#         }

#     @staticmethod
#     def set_session_data(request, username: str, user_id: str, is_admin: bool, uid: str) -> Tuple[str, Dict]:
#         """
#         Create a new session and return both session_id and cookie settings.
#         Returns: Tuple of (session_id, cookie_settings)
#         """
#         try:
#             session_id = UserSessionManager._generate_session_id()
#             current_time = datetime.utcnow()
#             expires_at = current_time + UserSessionManager.SESSION_DURATION
            
#             user_data = json.dumps({
#                 "_name": username,
#                 "_id": user_id,
#                 "_isAdmin": is_admin,
#                 "_uid": uid
#             })
            
#             # Invalidate existing sessions
#             invalidate_query = """
#                 UPDATE sessions 
#                 SET is_active = 0 
#                 WHERE JSON_VALUE(user_data, '$._uid') = %s
#                 AND is_active = 1;
#             """
#             db.update(invalidate_query, [uid])
            
#             # Insert new session
#             insert_query = """
#                 INSERT INTO sessions (session_id, user_data, expires_at, is_active)
#                 VALUES (%s, %s, %s, 1);
#             """
#             db.post_data(insert_query, [session_id, user_data, expires_at])
            
#             # Return both session_id and cookie settings
#             cookie_settings = UserSessionManager._get_cookie_settings(expires_at)
#             return session_id, cookie_settings
            
#         except Exception as e:
#             logger.error(f"Failed to create session: {e}")
#             raise InternalServerError("Failed to create session")

#     @staticmethod
#     def get_session_data(request) -> Optional['AuthUser']:
#         try:
#             session_id = request.COOKIES.get(UserSessionManager.COOKIE_NAME)
            
#             if not session_id:
#                 logger.debug("No session ID found in request")
#                 return None
            
#             query = """
#                 SELECT user_data, expires_at 
#                 FROM sessions 
#                 WHERE session_id = %s 
#                     AND is_active = 1 
#                     AND expires_at > GETDATE();
#             """
#             result = db.get_data(query, [session_id])
            
#             if not result:
#                 logger.debug("No valid session found")
#                 return None
            
#             # Refresh session expiration if it's close to expiring
#             session_data = result[0]
#             expires_at = session_data['expires_at']
#             if datetime.utcnow() + timedelta(hours=1) > expires_at:
#                 new_expires = datetime.utcnow() + UserSessionManager.SESSION_DURATION
#                 refresh_query = """
#                     UPDATE sessions 
#                     SET expires_at = %s 
#                     WHERE session_id = %s;
#                 """
#                 db.update(refresh_query, [new_expires, session_id])
            
#             user_data = json.loads(session_data['user_data'])
#             return AuthUser(**user_data)
            
#         except Exception as e:
#             logger.error(f"Error retrieving session: {e}")
#             return None

#     @staticmethod
#     def clear_session_data(request) -> None:
#         try:
#             session_id = request.COOKIES.get(UserSessionManager.COOKIE_NAME)
#             if session_id:
#                 query = """
#                     UPDATE sessions 
#                     SET is_active = 0 
#                     WHERE session_id = %s;
#                 """
#                 db.update(query, [session_id])
#                 logger.info(f"Session {session_id} invalidated")
#         except Exception as e:
#             logger.error(f"Error clearing session: {e}")
#             # raise InternalServerError("Failed to clear session")