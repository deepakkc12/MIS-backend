import os
import logging
from typing import Optional
from datetime import datetime, timedelta
import uuid

from ..services.Authentication import User
from ..utils.db import db
from ..utils.exceptions import AuthenticationError, InternalServerError
from ..utils.contexts import propagate_errors
from ..utils.helpers import get_current_date

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserSessionManager:
    """
    Session manager that uses database storage instead of Django's default session management.
    Requires a Sessions table with the following schema:
    
    CREATE TABLE Sessions (
        session_id VARCHAR(64) PRIMARY KEY,
        user_data JSON NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL,
        is_active BOOLEAN DEFAULT TRUE
    );
    """
    
    SESSION_DURATION = timedelta(hours=24)  # Configure session duration
    
    @staticmethod
    def _generate_session_id() -> str:
        """Generate a unique session ID."""
        return str(uuid.uuid4())
    
    @staticmethod
    def set_session_data(request, username: str, user_id: str, is_admin: bool, uid: str) -> None:
        """
        Create a new session in the database with user data.
        """
        try:
            session_id = UserSessionManager._generate_session_id()
            current_time = datetime.utcnow()
            expires_at = current_time + UserSessionManager.SESSION_DURATION
            
            # Prepare user data as a dictionary
            user_data = {
                "_name": username,
                "_id": user_id,
                "_isAdmin": is_admin,
                "_uid": uid
            }
            
            # First, invalidate any existing active sessions for this user
            invalidate_query = """
                UPDATE Sessions 
                SET is_active = FALSE 
                WHERE user_data->>'_uid' = %s AND is_active = TRUE;
            """
            db.execute(invalidate_query, [uid])
            
            # Insert new session
            insert_query = """
                INSERT INTO Sessions (session_id, user_data, expires_at, is_active)
                VALUES (%s, %s, %s, TRUE);
            """
            db.execute(insert_query, [session_id, user_data, expires_at])
            
            # Store session_id in request for future reference
            request.session_id = session_id
            
            logger.info(f"New session created for user: {username}")
            
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            raise InternalServerError("Failed to create session")
    
    @staticmethod
    def get_session_data(request) -> Optional['User']:
        """
        Retrieve session data from database and return User instance if valid.
        """
        try:
            # Get session_id from request
            session_id = getattr(request, 'session_id', None)
            if not session_id:
                # Try to get session_id from request headers
                session_id = request.headers.get('X-Session-ID')
            
            if not session_id:
                logger.debug("No session ID found in request")
                return None
            
            # Query for active session
            query = """
                SELECT user_data 
                FROM Sessions 
                WHERE session_id = %s 
                    AND is_active = TRUE 
                    AND expires_at > NOW();
            """
            result = db.get_data(query, [session_id])
            
            if not result:
                logger.debug("No valid session found")
                return None
            
            user_data = result[0]['user_data']
            return User(**user_data)
            
        except Exception as e:
            logger.error(f"Error retrieving session: {e}")
            return None
    
    @staticmethod
    def clear_session_data(request) -> None:
        """
        Invalidate the current session in the database.
        """
        try:
            session_id = getattr(request, 'session_id', None)
            if session_id:
                query = """
                    UPDATE Sessions 
                    SET is_active = FALSE 
                    WHERE session_id = %s;
                """
                db.execute(query, [session_id])
                delattr(request, 'session_id')
                logger.info(f"Session {session_id} invalidated")
        except Exception as e:
            logger.error(f"Error clearing session: {e}")
            raise InternalServerError("Failed to clear session")
    
    @staticmethod
    def cleanup_expired_sessions() -> None:
        """
        Utility method to clean up expired sessions.
        Should be run periodically (e.g., via cron job)
        """
        try:
            query = """
                DELETE FROM Sessions 
                WHERE expires_at < NOW() 
                OR is_active = FALSE;
            """
            db.execute(query)
            logger.info("Cleaned up expired sessions")
        except Exception as e:
            logger.error(f"Error cleaning up sessions: {e}")