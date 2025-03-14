import pyodbc
import logging
from typing import Generator, List, Dict, Optional, Any
from contextlib import contextmanager
from .connection import ConnectionManager
from .exceptions import DatabaseError, TransactionError
from .abstracts import DatabaseInterface
from .config import DatabaseConfig

logger = logging.getLogger(__name__)


def get_connection_string(server,database,username,password):
                
    connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"TRUST_SERVER_CERTIFICATE=yes;"
)
    return connection_string


server="103.12.1.191\SQL2022,61254"
db_name="TestingRestoran"
username="sa"
password="infopace"


class DB():

    connection_string = get_connection_string(server=server,database=db_name,username=username,password=password)

    connection = None

    active_connections = 0

    trans_connections = 0


    @classmethod    
    def open_connection(cls)->pyodbc.Connection:

        if (cls.active_connections == 0):
            cls.active_connections  += 1
            cls.connection =  pyodbc.connect(
                cls.connection_string,
                timeout=30
            )
            return cls.connection
        else:
            cls.active_connections  += 1

            return cls.connection
        

    @classmethod
    def close_connection(cls)->bool:

        if cls.connection:
            try:
                cls.connection.close()
                cls.active_connections = cls.active_connections -1
                logger.info("Connection closed successfully")
            except pyodbc.Error as e:
                logger.error(f"Error closing connection: {e}")
        else:
            cls.active_connections = cls.active_connections -1

    
    @contextmanager
    @classmethod
    def db_connection(cls) -> Generator[pyodbc.Connection, None, None]:
        connection = None
        try:
            connection = cls.open_connection()
            yield connection
        except Exception as e:
            raise DatabaseError(f"Database operation failed: {e}")
        finally:
           cls.close_connection()

    
    @classmethod
    def execute(cls,query,data):
       
     try:  
            connection = cls.open_connection()
            
            cursor = connection.cursor()

            cursor.execute(query,data)
            
            connection.commit()

            cls.close_connection()

     except  Exception as e:
         logger.error(f"get_data error: {e}")
         raise DatabaseError(f"Failed to execute query: {e}")
         

    @classmethod
    def get_data(cls, query: str, data: Optional[tuple] = []) -> List[Dict]:
        """Enhanced data fetching with connection pooling."""

        connection = None
        try:
            connection = cls.open_connection()
            cursor = connection.cursor()
            cursor.execute(query, data)
            columns = [column[0] for column in cursor.description]
            cls.close_connection()
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        except Exception as e:

            cls.close_connection()
            logger.error(f"get_data error: {e}")

            raise DatabaseError(f"Failed to fetch data: {e}")
        

    @contextmanager
    @classmethod
    def transaction(cls):
       try: 
        cls.start_transaction()
        yield
        cls.commit_transaction()

       except Exception as e:
           logger.error(f"Error Occured in transaction .current transaction count {cls.trans_connections}")

           cls.execute("ROLLBACK TRANSACTION")
       finally :
            cls.commit_transaction()

    
    @classmethod
    def start_transaction(cls):
        connection = None 
        try:
            connection = cls.open_connection()

            if cls.trans_connections == 0:

                cls.trans_connections += 1
                connection.execute("BEGIN TRANSACTION")

            else:
                cls.trans_connections +=1

        except Exception as e:
            logger.error(f"transaction error: {e}")

            raise DatabaseError(f"Failed inside transaction block: {e}")
        



    @classmethod
    def commit_transaction(cls):

        if cls.trans_connections == 1:
            cls.execute("Commit")
            return True

        cls.trans_connections -= 1
