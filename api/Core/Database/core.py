import logging
from typing import Generator, List, Dict, Optional, Any
from contextlib import contextmanager
import pyodbc
from .connection import ConnectionManager
from .exceptions import DatabaseError, TransactionError
from .abstracts import DatabaseInterface
from .config import DatabaseConfig

logger = logging.getLogger(__name__)

class Database(DatabaseInterface):
    """Unified database class with connection pooling and enhanced error handling."""

    def __init__(self, query_timeout: int = 300, db_config: DatabaseConfig = None):
        self.db_config = db_config
        self._connection_manager = ConnectionManager(self.db_config)
        self.query_timeout = query_timeout

    def get_db_connection(self) -> pyodbc.Connection:
        """Get a connection from the connection pool with configured timeout."""
        try:
            connection = self._connection_manager.get_connection()
            connection.timeout = self.query_timeout
            return connection
        except Exception as e:
            logger.error(f"Connection error: {e}")
            raise DatabaseError(f"Failed to establish database connection: {e}")

    @contextmanager
    def db_connection(self) -> Generator[pyodbc.Connection, None, None]:
        """Context manager for non-transactional database operations."""
        connection = None
        try:
            connection = self.get_db_connection()
            # Ensure autocommit is True for non-transactional operations
            connection.autocommit = True
            yield connection
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise DatabaseError(f"Database operation failed: {e}")
        finally:
            if connection:
                try:
                    self._connection_manager.release_connection(connection)
                except Exception as release_error:
                    logger.error(f"Error releasing connection: {release_error}")
                    try:
                        connection.close()
                    except Exception as close_error:
                        logger.error(f"Error closing connection: {close_error}")

    @contextmanager
    def transaction(self) -> Generator['TransactionConnection', None, None]:
        """Enhanced transaction context manager with proper transaction handling."""
        
        connection = None

        try:
            connection = self.get_db_connection()
            cursor = connection.cursor()
            
            # Begin transaction through connection manager
            self._connection_manager.begin_transaction(connection)
            
            # Configure timeouts
            cursor.execute(f"SET QUERY_GOVERNOR_COST_LIMIT {self.query_timeout * 1000}")
            cursor.execute(f"SET LOCK_TIMEOUT {self.query_timeout * 1000}")
            
            # Create transaction connection bundle
            trans_connection = self.TransactionConnection(connection, cursor)
            
            yield trans_connection
            
            # Commit through connection manager if no exceptions
            self._connection_manager.commit_transaction(connection)
            
        except Exception as e:
            if connection:
                try:
                    # Rollback through connection manager
                    self._connection_manager.rollback_transaction(connection)
                except Exception as rollback_error:
                    logger.error(f"Transaction rollback error: {rollback_error}")
            
            if 'timeout expired' in str(e).lower():
                logger.error(f"Query timeout after {self.query_timeout} seconds: {e}")
                raise TransactionError(f"Query timed out after {self.query_timeout} seconds.")
            
            raise TransactionError(f"Transaction failed: {e}")
        
        finally:
            if connection:
                try:
                    self._connection_manager.release_connection(connection)
                except Exception as release_error:
                    logger.error(f"Error releasing transaction connection: {release_error}")
                    try:
                        connection.close()
                    except Exception as close_error:
                        logger.error(f"Error closing transaction connection: {close_error}")



    def get_data(self, query: str, data: Optional[tuple] = []) -> List[Dict]:
        """Enhanced data fetching with connection pooling."""
        try:
            with self.db_connection() as connection:
                # print(f"connection string......................{self.db_config.connection_string}")
                cursor = connection.cursor()
                cursor.execute(query, data)
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"get_data error: {e}")
            raise DatabaseError(f"Failed to fetch data: {e}")

    def post_data(self, query: str, data: Optional[tuple] = [], primary_column: str = 'ID') -> Optional[int]:
        """Enhanced data insertion with connection pooling."""
        try:
            with self.db_connection() as connection:
                cursor = connection.cursor()
                
                if not query.strip() or not isinstance(query, str):
                    raise ValueError("Query must be a non-empty string")
                            
                normalized_query = query.strip()
                upper_query = normalized_query.upper()
                
                if not upper_query.startswith('INSERT'):
                    raise ValueError("Query must be an INSERT statement")
                    
                # Handle different types of INSERT statements
                if 'DEFAULT VALUES' in upper_query:
                    modified_query = normalized_query.replace(
                        'DEFAULT VALUES',
                        f"OUTPUT INSERTED.{primary_column} DEFAULT VALUES",
                        1
                    )
                    
                elif 'VALUES' in upper_query:
                    before_values, after_values = normalized_query.split('VALUES', maxsplit=1)
                    if not after_values:
                        raise ValueError("Malformed VALUES clause in INSERT statement")
                        
                    modified_query = (
                        f"{before_values} "
                        f"OUTPUT INSERTED.{primary_column} "
                        f"VALUES{after_values}"
                    )


                elif 'SELECT' in upper_query:
                    # Handle INSERT ... SELECT statements
                    select_pos = upper_query.find('SELECT')
                    modified_query = (
                        f"{normalized_query[:select_pos]} "
                        f"OUTPUT INSERTED.{primary_column} "
                        f"{normalized_query[select_pos:]}"
                    )
                    
                else:
                    raise ValueError("Unsupported INSERT statement format")
                
                # print(f"modified_query.....{modified_query}")
                # print(f"modified_query.....{data}")
                

                
                cursor.execute(modified_query, data)
                
                row = cursor.fetchone()
                inserted_id = row[0] if row else None



                
                # if inserted_id is None:
                #     cursor.execute("SELECT SCOPE_IDENTITY()")
                #     inserted_id = cursor.fetchone()[0]

                connection.commit()
                if inserted_id is None:
                    raise DatabaseError("Insertion Failed")
                return inserted_id
        except Exception as e:
            logger.error(f"post_data error: {e}")
            raise DatabaseError(f"Failed to insert data: {e}")
        

    def update(self, query: str, data: Optional[tuple] = []) -> int:
        """Enhanced update operation with connection pooling."""
        try:
            with self.db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, data)
                affected_rows = cursor.rowcount
                connection.commit()
                return affected_rows
        except Exception as e:
            logger.error(f"update error: {e}")
            raise DatabaseError(f"Failed to update data: {e}")
        
    def execute(self, query: str,data = []):
        try:
            with self.db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, data)
                # affected_rows = cursor.rowcount
                connection.commit()
                return 
        except Exception as e:
            logger.error(f"update error: {e}")
            raise DatabaseError(f"Failed to update data: {e}")

    def delete(self, query: str, data: Optional[tuple] = []) -> int:
        """Enhanced delete operation with connection pooling."""
        try:
            with self.db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, data)
                affected_rows = cursor.rowcount
                connection.commit()
                return affected_rows
        except Exception as e:
            logger.error(f"delete error: {e}")
            raise DatabaseError(f"Failed to delete data: {e}")
        

    
    class TransactionConnection:
        """Helper class for transaction operations with timeout handling."""
        def __init__(self, connection: pyodbc.Connection, cursor: pyodbc.Cursor):
            self.connection = connection
            self.cursor = cursor
            self._active = True

        def _handle_timeout_error(self, e: Exception, operation: str):
            """Handle timeout-specific errors with detailed logging"""
            if 'timeout expired' in str(e).lower():
                logger.error(f"Query timeout during {operation}: {e}")
                self._active = False
                raise TransactionError(
                    f"Query timed out during {operation}. Consider:\n"
                    "1. Breaking down the query into smaller chunks\n"
                    "2. Adding appropriate indexes\n"
                    "3. Optimizing the query\n"
                    "4. Increasing the timeout value if necessary"
                )
            raise e

        def post_data(self, query: str, data: Optional[list] = [], primary_column='id') -> Optional[int]:
            """Execute INSERT query with timeout handling."""
            if not self._active:
                raise TransactionError("Transaction is no longer active")
            
            try:
                if not query.strip() or not isinstance(query, str):
                    raise ValueError("Query must be a non-empty string")
                            
                normalized_query = query.strip()
                upper_query = normalized_query.upper()
                
                if not upper_query.startswith('INSERT'):
                    raise ValueError("Query must be an INSERT statement")
                    
                # Handle different types of INSERT statements
                if 'DEFAULT VALUES' in upper_query:
                    modified_query = normalized_query.replace(
                        'DEFAULT VALUES',
                        f"OUTPUT INSERTED.{primary_column} DEFAULT VALUES",
                        1
                    )
                    
                elif 'VALUES' in upper_query:
                    before_values, after_values = normalized_query.split('VALUES', maxsplit=1)
                    if not after_values:
                        raise ValueError("Malformed VALUES clause in INSERT statement")
                        
                    modified_query = (
                        f"{before_values} "
                        f"OUTPUT INSERTED.{primary_column} "
                        f"VALUES{after_values}"
                    )
                    
                elif 'SELECT' in upper_query:
                    # Handle INSERT ... SELECT statements
                    select_pos = upper_query.find('SELECT')
                    modified_query = (
                        f"{normalized_query[:select_pos]} "
                        f"OUTPUT INSERTED.{primary_column} "
                        f"{normalized_query[select_pos:]}"
                    )
                    
                else:
                    raise ValueError("Unsupported INSERT statement format")
                
                self.cursor.execute(modified_query, data)
                
                row = self.cursor.fetchone()
                if row:
                    return row[0]
                
                self.cursor.execute("SELECT SCOPE_IDENTITY()")
                return self.cursor.fetchone()[0]
            except pyodbc.Error as e:
                self._handle_timeout_error(e, "data insertion")

        def get_data(self, query: str, data: Optional[list] = []) -> list:
            """Execute SELECT query with timeout handling."""
            if not self._active:
                raise TransactionError("Transaction is no longer active")
            try:
                self.cursor.execute(query, data)
                return [dict(zip([col[0] for col in self.cursor.description], row))
                        for row in self.cursor.fetchall()]
            except pyodbc.Error as e:
                self._handle_timeout_error(e, "data fetching")


        def update(self, query: str, data: Optional[tuple] = None) -> int:
            """Enhanced update operation with connection pooling."""
            
            if not self._active:
                raise TransactionError("Transaction is no longer active")
            
            try:
                self.cursor.execute(query, data)
                affected_rows = self.cursor.rowcount
                return affected_rows
            except Exception as e:
                logger.error(f"update error: {e}")
                raise DatabaseError(f"Failed to update data: {e}")
            
        def delete(self, query: str, data: Optional[tuple] = None) -> int:
            """Enhanced delete operation with connection pooling."""
            if not self._active:
                raise TransactionError("Transaction is no longer active")
            
            try:
                self.cursor.execute(query, data)
                affected_rows = self.cursor.rowcount
                return affected_rows
            except Exception as e:
                logger.error(f"delete error: {e}")
                raise DatabaseError(f"Failed to delete data: {e}")
            
        def execute(self, query: str,data = []):

            if not self._active:
                raise TransactionError("Transaction is no longer active")
            try:

                self.cursor.execute(query, data)

                return 
            except Exception as e:
                logger.error(f"update error: {e}")
                raise DatabaseError(f"Failed to update data: {e}")