import uuid

id = uuid.uuid4().int
id2 =uuid.uuid4().int & (1<<64)-1
print(id)
print(id2)
