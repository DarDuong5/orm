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
print(User._pk)
# id

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

# Testing table creation
# print(User.create_table())
# CREATE TABLE user (id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER)

# Testing insert
u = User(id=1, name='Darin', age=21)
sql, values = u._insert()
print(sql)
# INSERT INTO user (id, name, age) VALUES (?, ?, ?)
print(values)
# (1, 'Darin', 21)

# Testing select single
sql, params = User._select(1)
print(sql)
# SELECT id, name, age FROM user WHERE id = ?
print(params)
# (1,)

# Testing select all
sql, params = User._select_all()
print(sql)
# SELECT id, name, age FROM user
print(params)
# ()

# Testing update
u = User(id=1, name='Darin', age=21)
sql, vals = u._update(age=22)
print(sql)
# UPDATE user SET age = ? WHERE id = ?
print(vals)
# (22, 1)

sql, vals = u._update(name='David', age=23)
print(sql)
# UPDATE user SET name = ?, age = ? WHERE id = ?
print(vals)
# ('David', 23, 1)

# sql, vals = u._update(name='David', age='invalid age')
# TypeError: 'invalid age' does not match to the type INTEGER

# Testing primary key requirement
# class User(Model):
#     id = IntegerField(primary_key=False)
#     name = StringField(max_length=30, nullable=False)
#     age = IntegerField(nullable=True)

# u = User(id=1, name='Darin', age=21)
# ValueError: 'user' requires at least one primary key

# testing delete
u = User(id=1, name='Darin', age=21)
sql, vals = u._delete()
print(sql)
# DELETE FROM user WHERE id = ?
print(vals)
# (1,)

# testing sqlite3 - creating table
Model.connect(':memory:')

class User(Model):
    id = IntegerField(primary_key=True)
    name = StringField(max_length=30)
print(User._connection)
User.create_table()

cursor = Model._connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

