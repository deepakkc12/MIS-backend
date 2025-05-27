import pyodbc
import logging
from typing import Optional
from contextlib import contextmanager
from threading import Lock
from .exceptions import DatabaseError
from .config import DatabaseConfig

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Thread-safe connection manager with proper transaction handling"""
    
    def __init__(self, db_config: DatabaseConfig):
        if db_config is None:
            raise DatabaseError("DatabaseConfig instance is required")
        
        self._db_config = db_config
        self._connection_pool = []
        self._max_pool_size = 0  
        self._lock = Lock()
        self._active_transactions = set()
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def _create_connection(self) -> pyodbc.Connection:
        try:
            connection_string = (
                f"DRIVER={self._db_config.driver};"
                f"SERVER={self._db_config.server};"
                f"DATABASE={self._db_config.database};"
                f"UID={self._db_config.username};"
                f"PWD={self._db_config.password};"
                f"TRUST_SERVER_CERTIFICATE={self._db_config.trust_server_certificate};"
            )
            
            connection = pyodbc.connect(
                connection_string,
                timeout=30,
                autocommit=True  # Start in autocommit mode by default
            )
            connection.timeout = 30
            
            # cursor = connection.cursor()
            # cursor.execute("SELECT DB_NAME() AS CurrentDatabase")
            # current_db = cursor.fetchone()[0]
            
            # logger.info(f"Created connection for database: {current_db}")
            
            return connection
        except pyodbc.Error as e:
            logger.error(f"Failed to create MSSQL connection: {e}")
            raise DatabaseError(f"Database connection failed: {e}")

    def get_connection(self) -> pyodbc.Connection:
        """Get a connection, considering transaction state"""
        with self._lock:
            # If connection has an active transaction, always create new
            if self._max_pool_size == 0:
                return self._create_connection()
                
            # Try to get an existing valid connection
            while self._connection_pool:
                connection = self._connection_pool.pop()
                if self._verify_connection(connection):
                    return connection
                else:
                    self._safe_close(connection)
            
            return self._create_connection()

    def release_connection(self, connection: pyodbc.Connection):
        """Release connection, handling transaction state"""
        with self._lock:
            try:
                # Check if connection has an active transaction
                if connection in self._active_transactions:
                    logger.info("Connection has active transaction - closing instead of pooling")
                    self._safe_close(connection)
                    self._active_transactions.remove(connection)
                    return
                
                # Normal pooling logic
                if self._max_pool_size > 0 and len(self._connection_pool) < self._max_pool_size:
                    if self._verify_connection(connection):
                        connection.autocommit = True  # Reset to autocommit before pooling
                        self._connection_pool.append(connection)
                    else:
                        self._safe_close(connection)
                else:
                    self._safe_close(connection)
            except Exception as e:
                logger.error(f"Error in release_connection: {e}")
                self._safe_close(connection)

    def begin_transaction(self, connection: pyodbc.Connection):
        """Mark connection as having an active transaction"""
        with self._lock:
            connection.autocommit = False
            self._active_transactions.add(connection)
            logger.info("Transaction begun on connection")

    def commit_transaction(self, connection: pyodbc.Connection):
        """Commit transaction and reset connection state"""
        with self._lock:
            try:
                connection.commit()
                connection.autocommit = True
                self._active_transactions.remove(connection)
                logger.info("Transaction committed successfully")
            except Exception as e:
                logger.error(f"Error committing transaction: {e}")
                raise

    def rollback_transaction(self, connection: pyodbc.Connection):
        """Rollback transaction and reset connection state"""
        with self._lock:
            try:
                connection.rollback()
                connection.autocommit = True
                self._active_transactions.remove(connection)
                logger.info("Transaction rolled back successfully")
            except Exception as e:
                logger.error(f"Error rolling back transaction: {e}")
                raise

    @contextmanager
    def transaction_scope(self):
        """Context manager for handling transactions properly"""
        connection = None
        try:
            connection = self.get_connection()
            self.begin_transaction(connection)
            yield connection
            self.commit_transaction(connection)
        except Exception:
            if connection:
                self.rollback_transaction(connection)
            raise
        finally:
            if connection:
                self.release_connection(connection)


    def _verify_connection(self, connection: Optional[pyodbc.Connection]) -> bool:
        """
        Verify if a connection is still valid
        
        Args:
            connection (Optional[pyodbc.Connection]): Connection to verify
        
        Returns:
            bool: True if connection is valid, False otherwise
        """
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Verify both connection and correct database
                    # cursor.execute("SELECT DB_NAME() AS CurrentDatabase")
                    # current_db = cursor.fetchone()[0]
                    
                    # # Additional verification
                    # is_valid = current_db == self._db_config.database
                    
                    # logger.info(f"Connection Verification: "
                    #             f"Expected {self._db_config.database}, "
                    #             f"Actual {current_db}, "
                    #             f"Valid: {is_valid}")
                    
                    return True
            except pyodbc.Error as e:
                logger.error(f"Connection verification failed: {e}")
                return False
        return False

    def _safe_close(self, connection: Optional[pyodbc.Connection]):
        """
        Safely close a connection
        
        Args:
            connection (Optional[pyodbc.Connection]): Connection to close
        """
        if connection:
            try:
                connection.close()
                # logger.info("Connection closed successfully")
            except pyodbc.Error as e:
                logger.error(f"Error closing connection: {e}")

    @contextmanager
    def connection_scope(self):
        """
        Context manager for automatic connection handling
        
        Yields:
            pyodbc.Connection: A managed database connection
        """
        connection = None
        try:
            connection = self.get_connection()
            yield connection
        finally:
            if connection:
                self.release_connection(connection)