import pytz
from ..Core import DatabaseModel,db,Field,FieldType
from datetime import datetime


class Model(DatabaseModel):

    def insert(self, connection=db):
        return super().insert(connection)
    
    def update(self, trans_connection=db):
        return super().update(trans_connection)
    
    def save(self, connection=db):
        return super().save(connection)

    @classmethod
    def list(cls, connection=db):
        return super().list(connection)
    
    @classmethod
    def filter(cls, connection=db, **kwargs):
        return super().filter(connection, **kwargs)

    def delete(self, connection=db):
        return super().delete(connection)
    
    @classmethod
    def find_by_id(cls, id, connection=db):
        return super().find_by_id(id, connection)
    
    @classmethod
    def serialized_list(cls, connection=db):
        return super().serialized_list(connection)
    
    @classmethod
    def serialized_filtered_list(cls, connection=db, **kwargs):
        return super().serialized_filtered_list(connection, **kwargs)

    @staticmethod
    def generate_tot():
        malaysia_tz = pytz.timezone("Asia/Kuala_Lumpur")
        malaysia_time = datetime.now(malaysia_tz)
        return float(malaysia_time.strftime("%H.%M"))
        # return float(datetime.now().strftime("%H.%M"))