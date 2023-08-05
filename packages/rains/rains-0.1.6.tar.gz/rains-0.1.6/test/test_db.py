
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from rains.db.rains_db import RainsDb
from rains.db.blueprint.sql_run_environment import SqlRunEnvironment
from rains.db.blueprint.sql_config import SqlConfig


db = RainsDb()
db.write(SqlRunEnvironment.init())
db.write(SqlConfig.add({
    'name': 'base', 
    'core_maxsize': 3, 
    'task_maxsize': 50
    }))

print(bool(db.read(SqlRunEnvironment.get())[0][1]))
print(type(bool(db.read(SqlRunEnvironment.get())[0][1])))
print(db.read(SqlConfig.get()))

db.commit()
db.quit()
