import pymssql
import json
from contextlib import contextmanager
from .exceptions import DatabaseError, NotFoundError
import logging
from typing import Optional
import os
from django.conf import settings

logger = logging.getLogger(__name__)

# Load the database configurations from JSON file
CONFIG_FILE_PATH = os.path.join(settings.BASE_DIR, 'config.json')

# def load_db_config():
#     try:
#         with open(CONFIG_FILE_PATH, 'r') as config_file:
#             return json.load(config_file)
#     except FileNotFoundError:
#         raise DatabaseError(f"Database configuration file not found at {CONFIG_FILE_PATH}")
#     except json.JSONDecodeError as e:
#         raise DatabaseError(f"Error decoding JSON configuration file: {e}")

# Load configurations
db_config = {}

class db:
    @staticmethod
    def get_db_connection():
        try:
            return pymssql.connect(
                server=db_config['DB_SERVER'],
                user=db_config['DB_USER'],
                password=db_config['DB_PASSWORD'],
                database=db_config['DB_NAME']
            )
        except pymssql.Error as e:
            logger.error(f"Connection error: {e}")
            raise DatabaseError(e)

    @staticmethod
    @contextmanager
    def db_connection():
        connection = db.get_db_connection()
        try:
            if connection is None:
                raise Exception("Failed to establish a database connection.")
            yield connection
        finally:
            if connection:
                connection.close()

    @staticmethod
    def post_data(query, data=None):
        try:
            with db.db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, data)
                connection.commit()
                cursor.execute("SELECT SCOPE_IDENTITY() AS id")
                inserted_id = cursor.fetchone()[0]
                return inserted_id
        except Exception as e:
            logger.error(f"Error occurred while posting: {e}")
            raise DatabaseError(f"Error occurred while posting: {e}")

    @staticmethod
    def get_data(query, data=None)->list[dict]:
        try:
            with db.db_connection() as connection:
                cursor = connection.cursor(as_dict=True)
                cursor.execute(query, data)
                result = cursor.fetchall()
                return result
        except Exception as e:
            logger.error(f"Error occurred while reading: {e}")
            raise DatabaseError(f"Error occurred while reading: {e}")
        
    @staticmethod
    def update(query, data=None):
        try:
            with db.db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, data)
                connection.commit()
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Error occurred while updating: {e}")
            raise DatabaseError(f"Error occurred while updating: {e}")
        

class TransactionError(Exception):
    """Custom exception for transaction-related errors"""
    pass

class TransactionConnection:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def post_data(self, query: str, data: Optional[list] = None) -> int:
        try:
            self.cursor.execute(query, data)
            self.cursor.execute("SELECT SCOPE_IDENTITY() AS id")
            return self.cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Error in post_data: {str(e)}")
            raise TransactionError(f"Error in post_data: {str(e)}")

    def get_data(self, query: str, data: Optional[list] = None) -> list:
        try:
            self.cursor.execute(query, data)
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error in get_data: {str(e)}")
            raise TransactionError(f"Error in get_data: {str(e)}")

@contextmanager
def transaction():
    """
    Transaction context manager that works with the existing db class.
    
    Usage:
        with transaction_scope() as trans:
            id1 = trans.post_data("INSERT INTO table1 VALUES (%s)", [value1])
            id2 = trans.post_data("INSERT INTO table2 VALUES (%s)", [value2])
    """
    connection = None
    trans_connection = None
    
    try:
        connection = db.get_db_connection()
        if connection is None:
            raise TransactionError("Failed to establish a database connection.")
        
        cursor = connection.cursor()
        trans_connection = TransactionConnection(connection, cursor)

        try:
            yield trans_connection
            connection.commit()
        except Exception as e:
            if connection:
                try:
                    connection.rollback()
                except Exception as rollback_error:
                    logger.error(f"Error during rollback: {str(rollback_error)}")
            raise TransactionError(f"Transaction failed: {e}")
    finally:
        if connection:
            try:
                connection.close()
            except Exception as close_error:
                logger.error(f"Error closing connection: {str(close_error)}")