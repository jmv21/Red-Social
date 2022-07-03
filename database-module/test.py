import uuid

from DB import *

create_db(initial_id=1000)

db = db_connect()

user_register('carlos', 'name', uuid.uuid4().int)
user_register('jose', 'name', uuid.uuid4().int)
user_register('david', 'name', uuid.uuid4().int)
user_register('charles', 'name', uuid.uuid4().int)

