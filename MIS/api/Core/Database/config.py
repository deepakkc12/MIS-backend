
from typing import Optional
import urllib.parse
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DatabaseConfig:
    """Singleton configuration class for database settings"""
    driver: str = '{ODBC Driver 17 for SQL Server}'
    server: str = None
    database: str = None
    username: str = None
    password: str = None
    # timeout: int = int(os.getenv('DB_TIMEOUT', '30'))
    # pool_size: int = int(os.getenv('DB_POOL_SIZE', '10'))
    # pool_timeout: int = int(os.getenv('DB_POOL_TIMEOUT', '30'))
    trust_server_certificate: str = 'yes'

    def __post_init__(self):
        # print(self)
        self._validate_config()

    def _validate_config(self):
        """Validate configuration parameters"""
        if not all([self.server, self.database, self.username, self.password]):
            raise ValueError("Missing required database configuration parameters")

    @property
    def connection_string(self) -> str:
        """Generate properly escaped connection string"""
        password = urllib.parse.quote_plus(self.password)
        return (
            f'DRIVER={self.driver};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'UID={self.username};'
            f'PWD={password};'
            # f'CONNECTION_TIMEOUT={self.timeout};'
            f'TRUST_SERVER_CERTIFICATE={self.trust_server_certificate};'
            f'MARS_Connection=yes;'
            # f'Pool_Size={self.pool_size};'
            # f'Pool_Timeout={self.pool_timeout}'
        )
    
def load_db_config(server,db,username,password) -> DatabaseConfig:
    """
    Load database configuration based on a specific prefix.
    """
    return DatabaseConfig(
        server=server,
        database=db,
        username=username,
        password=password,
    )