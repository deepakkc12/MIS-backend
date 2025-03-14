from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
import logging
from .metaclass import ModelMetaclass
from ..Database import Database,DatabaseError

logger = logging.getLogger(__name__)

T = TypeVar('T', bound='DatabaseModel')

class BaseModel(ABC, metaclass=ModelMetaclass):
    """
    Base class for all database models.
    Provides core ORM functionality with proper inheritance support.
    """
    
    def __init__(self, **kwargs):
        self._is_new = True
        
        for field_name, field in self.__class__._fields.items():
            if field.auto_increment and field_name not in kwargs:
                setattr(self, field_name, None)
            else:
                setattr(self, field_name, kwargs.get(field_name, field.default))
        
        unknown_fields = set(kwargs) - set(self.__class__._fields)
        # print(unknown_fields)
        if unknown_fields:
            raise ValueError(f"Unknown fields: {', '.join(unknown_fields)}")
    
    def validate(self) -> None:
        for field_name, field_def in self.__class__._fields.items():

            value = getattr(self, field_name, None)
            
            field_def.validate_value(value, field_name)
    
    @classmethod
    def get_table_name(cls) -> str:
        return getattr(cls, '_table_name', cls.__name__)
    
    @property
    def table_name(self) -> str:
        return getattr(self.__class__, '_table_name', self.__class__.__name__)
    
    @classmethod
    def get_fields(cls) -> List[str]:
        return list(cls._fields.keys())
    
    @classmethod
    def get_primary_key_field(cls) -> str:
        if not hasattr(cls, '_primary_key'):
            cls._set_primary_key()
        return cls._primary_key
    
    @classmethod
    def is_auto_increment_pk(cls) -> bool:
        pk_field = cls._fields[cls.get_primary_key_field()]
        return pk_field.auto_increment
    
    @classmethod
    def get_non_auto_increment_fields(cls) -> List[str]:
        """Returns a list of fields that are NOT auto-incrementing."""
        if not hasattr(cls, "_fields"):
            return []
        
        return [
            field_name for field_name, field in cls._fields.items()
            if not getattr(field, "auto_increment", False)  # Default to False if attribute is missing
        ]
    
    def get_primary_key_value(self) -> Any:
        return getattr(self, self.__class__.get_primary_key_field())
    
    def serialize(self) -> Dict[str, Any]:
        data = {}
        for field_name in self.get_fields():
            field = self.__class__._fields[field_name]
            if not field.is_secured:
                value = getattr(self, field_name, None)
                if value is not None:
                    if isinstance(value, (date, datetime)):
                        data[field_name] = value
                    else:
                        data[field_name] = value
        return data

    def to_dict(self) -> Dict[str, Any]:
        self.validate()
        data = {}
        for field_name in self.get_fields():
            field = self.__class__._fields[field_name]
            
            value = getattr(self, field_name, None)
            if value is not None:
                if isinstance(value, (date, datetime)):
                    data[field_name] = value
                else:
                    data[field_name] = value
        return data
    
    @classmethod
    def _set_primary_key(cls):
        """
        Set the primary key field, taking inheritance into account.
        """
        # Get all bases that might have fields
        bases = [cls] + list(cls.__bases__)
        primary_key_found = False
        
        for base in bases:
            if hasattr(base, '_fields'):
                for field_name, field in base._fields.items():

                    if field.is_primary:

                        if not primary_key_found:
                            cls._primary_key = field_name
                            primary_key_found = True
                        else:
                            # If primary key is already found in a parent class,
                            # remove is_primary from the child class field
                            if base == cls:
                                field.is_primary = False

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """
        Initialize subclass with proper field inheritance.
        """
        super().__init_subclass__(**kwargs)
        
        # Collect fields from all parent classes
        all_fields = {}
        for base in reversed(cls.__mro__):
            if hasattr(base, '_fields'):
                all_fields.update(base._fields)
        
        # Set the combined fields on the class
        if not hasattr(cls, '_fields'):
            cls._fields = {}
        cls._fields.update(all_fields)
        
        # Set primary key after fields are combined
        cls._set_primary_key()



class DatabaseModel(BaseModel):
    
    """
    Concrete database model implementation.
    
    Provides database operations using the configured database connection.
    
    """
    def insert(self, connection=Database) -> None:
        """Insert a new record into the database."""
        self.validate()
        data = self.to_dict()
        primary_key_field = self.__class__.get_primary_key_field()
        is_auto_increment = self.__class__.is_auto_increment_pk()

        try:
            if is_auto_increment:
                # Exclude the primary key field for auto-increment
                fields = [f for f in self.get_fields() if f != primary_key_field and f in data]
            else:
                # Include all fields including primary key
                fields = [f for f in self.get_fields() if f in data]
            
            values = [data[f] for f in fields]
            columns = ", ".join(fields)
            placeholders = ", ".join(["?"] * len(fields))
            
            query = f"INSERT INTO {self.get_table_name()} ({columns}) VALUES ({placeholders})"

            # print(f"primarykey:{primary_key_field}")
            
            if connection:
                if is_auto_increment:
                    # print(query)
                    new_id = connection.post_data(query, values,primary_column= primary_key_field)
                    # print(f"new_id..............................{new_id}")
                    if new_id:
                        setattr(self, primary_key_field, new_id)
                    return new_id
                else:
                    new_id = connection.post_data(query, values,primary_column= primary_key_field)
                     
                    if new_id:
                        return new_id
                    else:
                        setattr(self,primary_key_field,None)

            # else:
            #     with Database.transaction() as trans:
            #         if is_auto_increment:
            #             new_id = trans.post_data(query, values, primary_key_field)
            #             if new_id:
            #                 setattr(self, primary_key_field, new_id)
            #             return new_id
            #         else:
            #             trans.post_data(query, values)
            
            self._is_new = False
            
        except Exception as e:
            logger.error(f"Failed to insert {self.__class__.__name__}: {str(e)}")
            raise

    def update(self, trans_connection=Database) -> None:
        """Update an existing record in the database."""
        self.validate()
        data = self.to_dict()
        primary_key_field = self.__class__.get_primary_key_field()
        primary_key_value = self.get_primary_key_value()

        if primary_key_value is None:
            raise ValueError("Cannot update record without primary key value")

        try:
            set_fields = [f for f in self.get_non_auto_increment_fields() if f != primary_key_field and f in data]
            
            if not set_fields:
                return
                
            set_values = [data[f] for f in set_fields]
            set_clause = ", ".join([f"{field} = ?" for field in set_fields])
            
            query = f"UPDATE {self.get_table_name()} SET {set_clause} WHERE {primary_key_field} = ?"
            values = set_values + [primary_key_value]
            
            if trans_connection:
                trans_connection.update(query, values)

            else:
                raise Exception("Connection required")
            # else:
            #     with Database.transaction() as trans:
            #         trans.update(query, values)

        except Exception as e:
            logger.error(f"Failed to update {self.__class__.__name__}: {str(e)}")
            raise

    
    def save(self, trans_connection=Database) -> None:
        """Save the record (either insert or update based on _is_new flag)."""
        if self._is_new:
            id = self.insert(trans_connection)
            if not id:
                raise Exception("Insertion Failed")
            # print(f"id......................{id}")
            return id
        else:
            self.update(trans_connection)

    @classmethod
    def bulk_create(cls: Type[T], instances: List[T]) -> None:
        if not instances:
            return
        try:
            with Database.transaction() as trans:
                for instance in instances:
                    instance.insert(trans_connection=trans)
        except Exception as e:
            logger.error(f"Bulk create failed: {str(e)}")
            raise
    
    @classmethod
    def list(cls: Type[T],connection=Database) -> List[T]:
        try:
            query = f"SELECT * FROM {cls.get_table_name()} WITH (NOLOCK)"
            rows = connection.get_data(query=query)
            return [cls(**row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to list {cls.__name__}: {str(e)}")
            raise
    
    @classmethod
    def find_by_id(cls: Type[T], id: Any,connection=Database) -> Optional[T]:
        try:    
            primary_key_field = cls.get_primary_key_field()
            query = f"SELECT * FROM {cls.get_table_name()} WITH (NOLOCK) WHERE {primary_key_field} = ?"
            rows = connection.get_data(query, [id])
            if rows:
                instance = cls(**rows[0])
                instance._is_new = False
                return instance
            return None
        except Exception as e:
            logger.error(f"Failed to find {cls.__name__} with {primary_key_field}={id}: {str(e)}")
            raise
    
    @classmethod
    def filter(cls: Type[T],connection=Database, **kwargs,) -> List[T]:
        if not kwargs:
            return cls.list(connection=connection)
                    
        where_clauses = []
        values = []
        
        for field_name, value in kwargs.items():
            if field_name in cls.get_fields():
                where_clauses.append(f"{field_name} = ?")
                values.append(value)
            else:
                logger.warning(f"Field '{field_name}' is not valid for {cls.__name__}")

        where_clause = " AND ".join(where_clauses)
        query = f"SELECT * FROM {cls.get_table_name()} WITH (NOLOCK) WHERE {where_clause}"

        # print(query)

        try:
            rows = connection.get_data(query, values)
            instances = []
            for row in rows:
                instance = cls(**row)
                instance._is_new = False
                instances.append(instance)
            return instances
        except Exception as e:
            logger.error(f"Failed to filter {cls.__name__}: {str(e)}")
            raise

    def delete(self: Type[T],connection =Database) -> None:
        try:
            primary_key_field = self.__class__.get_primary_key_field()
            primary_key_value = self.get_primary_key_value()
            query = f"DELETE FROM {self.get_table_name()} WHERE {primary_key_field} = ?"
            connection.delete(query, (primary_key_value))
            logger.info(f"{self.__class__.__name__} with ID {primary_key_value} deleted successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to delete {self.__class__.__name__} with ID {primary_key_value}: {str(e)}")
            raise
