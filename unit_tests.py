from fields import *
from model import *

# Field testing
class Point:
    name: str = StringField(max_length=10)
    x: int = IntegerField()
    y: int = IntegerField()

primary = StringField(primary_key=True)
print(primary.primary_key) # True

p = Point.__new__(Point)
p.name, p.x, p.y = 'A', 1, 2
print(p.name, p.x, p.y) # A 1 2
# p.name = 'Name Too Long' # throws error
# p.x = 'Not an integer' # throws error
# p.y = 'Also not an integer' # throws error

# Model testing
class User(metaclass=ModelMeta):
    id = IntegerField(primary_key=True)
    name = StringField(max_length=30)
    non_field = 10

print(User._fields) 
# {'id': <fields.IntegerField object at ..., 'name': <fields.StringField object at ...>}
print(User._table_name) 
# user

# Base model testing
class User(Model):
    id = IntegerField(primary_key=True)
    name = StringField(max_length=30)
    count = IntegerField(default=0)
    note = StringField(default=None)

u = User(id=1, name='Darin')
print(u.id, u.name, u.count, u.note)
# 1 Darin 0 None
# u = User(id='bad', name='Darin') # invalid type for id
# throws error
# u = User(nme='Darin') # mispelled field which does not exist
# throws error
# u = User(id=1) # missing 'name' with no default value
# # throws error

class User(Model):
    id = IntegerField(primary_key=True)
    name = StringField(max_length=30, nullable=False)
    age = IntegerField(nullable=True)

print(User._create_table())
# CREATE TABLE user (id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER)

u = User(id=1, name='Darin', age=21)
sql, values = u._insert()
print(sql)
# INSERT INTO user (id, name, age) VALUES (?, ?, ?)
print(values)
# (1, 'Darin', 21)
