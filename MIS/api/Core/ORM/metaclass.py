from abc import ABCMeta
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from .fields import Field

class ModelMetaclass(ABCMeta):
    """Metaclass for database models that handles field definitions"""
    
    def __new__(mcs, name, bases, attrs):
        # Skip processing for BaseModel itself
        if name == 'BaseModel':
            return super().__new__(mcs, name, bases, attrs)
            
        # Collect field definitions
        fields = {}
        
        # Collect fields from base classes
        for base in bases:
            if hasattr(base, '_fields'):
                fields.update(base._fields)
                
        # Collect fields from current class
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
                    
        # Store fields in class
        attrs['_fields'] = fields
        
        return super().__new__(mcs, name, bases, attrs)