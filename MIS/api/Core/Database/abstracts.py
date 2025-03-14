import logging
from abc import ABC, abstractmethod
from typing import Generator, List, Dict, Optional, Any
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class DatabaseInterface(ABC):
    """Abstract base class for database operations."""


    # @abstractmethod
    # @contextmanager
    # def db_connection(self) -> Generator[Any, None, None]:
    #     """Context manager for database connection."""
    #     pass

    @abstractmethod
    def get_data(self, query: str, data: Optional[tuple] = None) -> List[Dict]:
        """Fetch data from the database."""
        pass

    @abstractmethod
    def post_data(self, query: str, data: Optional[tuple] = None, primary_column: str = 'id') -> Optional[int]:
        """Post data to the database and return the inserted ID."""
        pass

    @abstractmethod
    def update(self, query: str, data: Optional[tuple] = None) -> int:
        """Execute an UPDATE or DELETE operation."""
        pass

    @contextmanager
    @abstractmethod
    def transaction(self) -> Generator['DatabaseInterface', None, None]:
        """Context manager for handling transactions."""
        pass
