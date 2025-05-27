import pyodbc
import logging
from typing import Optional
from contextlib import contextmanager
from threading import Lock
from .exceptions import DatabaseError
from .config import DatabaseConfig

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Thread-safe connection manager with connection pooling"""
    
    def __init__(self, db_config: DatabaseConfig):
        """
        Initialize ConnectionManager with specific database configuration
        
        Args:
            db_config (DatabaseConfig): Configuration for database connection
        """
        if db_config is None:
            raise DatabaseError("DatabaseConfig instance is required")
        
        self._db_config = db_config
        self._connection_pool = []
        self._max_pool_size = 5  # Configurable pool size
        self._lock = Lock()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Log initialization details
        # logger.info(f"Initializing ConnectionManager for database: {db_config.database}")
        # logger.info(f"Server: {db_config.server}")

    def _create_connection(self) -> pyodbc.Connection:
        """
        Create a new database connection with proper error handling
        
        Returns:
            pyodbc.Connection: A new database connection

        Raises:
            DatabaseError: If connection creation fails

        """
        try:
            # Explicitly generate connection string
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
                timeout=30  # Connection timeout in seconds
            )
            connection.timeout = 30  # Query timeout
            
            # Verify the connected database
            cursor = connection.cursor()
            cursor.execute("SELECT DB_NAME() AS CurrentDatabase")
            current_db = cursor.fetchone()[0]
            
            logger.info(f"Created connection for database: {current_db}")
            
            return connection
        except pyodbc.Error as e:
            logger.error(f"Failed to create MSSQL connection: {e}")
            raise DatabaseError(f"Database connection failed: {e}")

    def get_connection(self) -> pyodbc.Connection:
        """
        Get a connection from the pool or create a new one
        
        Returns:
            pyodbc.Connection: A valid database connection
        """
        with self._lock:
            # Try to get an existing valid connection
            while self._connection_pool:
                connection = self._connection_pool.pop()
                if self._verify_connection(connection):
                    return connection
                else:
                    self._safe_close(connection)
                
            # Create new connection if pool is empty
            return self._create_connection()

    def release_connection(self, connection: pyodbc.Connection):
        """
        Return a connection to the pool
        
        Args:
            connection (pyodbc.Connection): Connection to be released
        """
        with self._lock:
            if len(self._connection_pool) < self._max_pool_size:
                if self._verify_connection(connection):
                    self._connection_pool.append(connection)
                else:
                    self._safe_close(connection)
            else:
                self._safe_close(connection)

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
                    cursor.execute("SELECT DB_NAME() AS CurrentDatabase")
                    current_db = cursor.fetchone()[0]
                    
                    # Additional verification
                    is_valid = current_db == self._db_config.database
                    
                    logger.info(f"Connection Verification: "
                                f"Expected {self._db_config.database}, "
                                f"Actual {current_db}, "
                                f"Valid: {is_valid}")
                    
                    return is_valid
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