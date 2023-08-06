import os
import sys
sys.path.append(r"C:\Users\Cheny\Documents\Python\PyPi_DoNotDelete\clioedb")
from clioedb.mydbconn import Connect_DB
filename = os.path.basename(__file__)
log_name = filename.split(".")[0] + '.log'

db_credential = {  #
    "user": "root",
    "password": "Belajar1",
    "host": "127.0.0.1",
    "db": "sql_store",
}
try:
    db = Connect_DB(db_credential)
    sql = "SELECT * FROM sql_store.customers;"
    rc = db.fetchone(sql)
    print(rc)
finally:
    db.close
