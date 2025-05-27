from .ORM import DatabaseModel,Field,FieldType
from .Database import load_db_config,Database

db_config = load_db_config(server="103.12.1.191\SQL2022,61254",db="MIS_DM_NDK",username="sa",password="infopace")

# db_config = load_db_config(server="localhost",db="r_pos_db",username="sa",password="admin1")

# POS_DB_SERVER = 103.12.1.191\SQL2022,61254
# POS_DB_DATABASE = KotDemo
# POS_DB_USERNAME = sa
# POS_DB_PASSWORD = infopace

db = Database(db_config=db_config)

__all__ = ['db','DatabaseModel','Field','FieldType']    