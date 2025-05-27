from enum import Enum
import logging
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from django.http import HttpRequest
from ...Core import db
from ...models.Models import Customers
from .InactiveCustomers import InActiveCustomers
from .PriorityCustomers import PriorityCustomers
from ...utils.exceptions import AuthenticationError, InternalServerError
from ...utils.contexts import propagate_errors
from ...utils.helpers import get_current_date,get_past_date

class ActiveCustomers:
    def count():
        query = """SELECT COunt(*) as ActiveCustomers from ActiveCustomers"""

        result = db.get_data(query=query)

        if not result:
            raise Exception("Count not got")
        
        return result[0]['ActiveCustomers']
    

    def list():
        query = """select """
