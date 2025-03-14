from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
import logging

logger = logging.getLogger(__name__)


class FieldType(Enum):
    """Supported database field types"""
    INTEGER = "INTEGER"
    STRING = "VARCHAR"
    TEXT = "TEXT"
    BOOLEAN = "BOOLEAN"
    DATETIME = "DATETIME"
    DATE = "DATE"
    TIME = "TIME"
    FLOAT = "FLOAT"
    BYTES = "BYTES"

@dataclass
class Field:
    """
    Represents a database field configuration.
    Handles field type validation and default value formatting.
    """
    field_type: FieldType
    nullable: bool = True
    max_length: Optional[int] = None
    default: Any = None
    unique: bool = False
    is_primary: bool = False
    auto_increment: bool = False
    is_secured: bool = False


    def __post_init__(self):
        """Validate field configuration after initialization"""
        if self.auto_increment:
            self._validate_auto_increment()
    
    def _validate_auto_increment(self):
        """Validate auto-increment field settings"""
        # if not self.is_primary:
        #     raise ValueError("Auto-increment can only be used with primary key fields")
        if self.field_type != FieldType.INTEGER:
            raise ValueError("Auto-increment can only be used with INTEGER fields")
        if self.nullable:
            self.nullable = False

    def _format_default(self) -> str:
        """Format default value for SQL query"""
        if isinstance(self.default, str):
            return f"'{self.default}'"
        if isinstance(self.default, bool):
            return str(self.default).upper()
        return str(self.default)
    
    def validate_value(self, value: Any, field_name: str) -> None:
        """
        Validate a value against the field's type and constraints
        
        Args:
            value: Value to validate
            field_name: Name of the field (for error messages)
        Raises:
            ValueError: If value violates field constraints
            TypeError: If value is of wrong type
        """
        if self.auto_increment and value is None:
            return
            
        if value is None:
            if not self.nullable:
                raise ValueError(f"Field '{field_name}' cannot be null")
            return
            
        self._validate_type(value, field_name)
        self._validate_constraints(value, field_name)

    def _validate_type(self, value: Any, field_name: str) -> None:
        if self.field_type == FieldType.INTEGER:
            try:
                # Attempt to convert to integer
                value = int(value)
            except (ValueError, TypeError) as e:
                raise TypeError(f"Field '{field_name}' must be an integer, but got {value!r}. Conversion failed: {e}")
            
        if self.field_type == FieldType.STRING:
            try:
                # Attempt to convert to integer
                value = str(value)
            except (ValueError, TypeError) as e:
                raise TypeError(f"Field '{field_name}' must be an string, but got {value!r}. Conversion failed: {e}")
        """Validate value type matches field type"""
        type_validators = {
            FieldType.FLOAT: ((float, int), "a number"),
            FieldType.TEXT: (str, "a string"),
            FieldType.BOOLEAN: (bool, "a boolean"),
            FieldType.DATETIME: ((datetime, date), "a datetime or date")
        }

        expected_type, type_name = type_validators.get(self.field_type, (object, "any type"))
        if not isinstance(value, expected_type):
            raise TypeError(f"Field '{field_name}' must be {type_name}")

    def _validate_constraints(self, value: Any, field_name: str) -> None:
        """Validate value meets field constraints"""
        if self.field_type in (FieldType.STRING, FieldType.TEXT):
            if self.max_length and len(value) > self.max_length:
                raise ValueError(f"Field '{field_name}' exceeds maximum length of {self.max_length}")