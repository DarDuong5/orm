from fields import *
from model import *

# ============ Test Classes with Metaclasses ============
class TestPoint(metaclass=ModelMeta):
    name: str = StringField(max_length=10, primary_key=True, nullable=False)
    x: int = IntegerField()
    y: int = IntegerField()

class TestUser(metaclass=ModelMeta):
    id: int = IntegerField(primary_key=True, nullable=False)
    name: str = StringField(max_length=30)
    age: int = IntegerField()
    count: int = IntegerField(default=0)
    note: str = StringField(default=None)

# ============ Field Tests ============
def test_field_types() -> None:
    string_field = StringField()
    assert isinstance(string_field, StringField)
    integer_field = IntegerField()
    assert isinstance(integer_field, IntegerField)

def test_primary_key() -> None:
    primary_int = IntegerField(primary_key=True)
    assert primary_int.primary_key == True

    not_primary_int = IntegerField()
    assert not_primary_int.primary_key == False

    primary_str = StringField(primary_key=True)
    assert primary_str.primary_key == True

    not_primary_str = StringField()
    assert not_primary_str.primary_key == False

def test_nullable() -> None:
    nullable_int = IntegerField(nullable=True)
    assert nullable_int.nullable == True

    not_nullable_int = IntegerField(nullable=False)
    assert not_nullable_int.nullable == False

    nullable_str = StringField(nullable=True)
    assert nullable_str.nullable == True

    not_nullable_str = StringField(nullable=False)
    assert not_nullable_str.nullable == False

def test_default() -> None:
    default_int = IntegerField(default=1)
    assert default_int.default == 1

    not_default_int = IntegerField()
    assert isinstance(not_default_int.default, object)

    default_str = StringField(default='')
    assert default_str.default == ''

    not_default_str = StringField()
    assert isinstance(not_default_str.default, object)

def test_setters() -> None:
    point = TestPoint.__new__(TestPoint)
    point.name, point.x, point.y = 'A', 1, 2
    assert point.name == 'A'
    assert point.x == 1
    assert point.y == 2

def test_validate() -> None:
    point = TestPoint.__new__(TestPoint)
    try: 
        point.name = "Name is too long"
        point.x = "Not an integer"
        point.y = "Also not an integer"
        assert False, 'Expected ValueError but none raised'
    except:
        pass

# ============ Test Classes with Base Models ============

class TestPoint(Model):
    name: str = StringField(max_length=10, primary_key=True, nullable=False)
    x: int = IntegerField()
    y: int = IntegerField()

class TestUser(Model):
    id: int = IntegerField(primary_key=True, nullable=False)
    name: str = StringField(max_length=30)
    age: int = IntegerField()
    count: int = IntegerField(default=0)
    note: str = StringField(default=None)

# ============ Model Tests ============

def test_model_attr() -> None:
    for field in TestPoint._fields.values():
        assert isinstance(field, Field) == True

    for field in TestUser._fields.values():
        assert isinstance(field, Field) == True

    assert TestPoint._table_name == 'testpoint'
    assert TestUser._table_name == 'testuser'

    assert TestPoint._pk == 'name'
    assert TestUser._pk == 'id'

def test_base_model() -> None:
    user = TestUser(id=1, name='Darin', age=21)
    assert user.id == 1
    assert user.name == 'Darin'
    assert user.age == 21
    assert user.count == 0
    assert user.note is None

def test_base_model_validation() -> None:
    try:
        TestPoint(name='Name too long') # provided string value exceeds the max length of string field
        assert False, 'Expected ValueError but got none'
    except ValueError:
        pass

    try:
        TestPoint(name=10) # invalid type (name should be str)
        assert False, 'Expected ValueError but got none'
    except TypeError:
        pass

    try:
        TestUser(id='invalid type', name='Darin') # invalid type (id should be int)
        assert False, 'Expected TypeError but got none'
    except TypeError:
        pass

    try:
        TestUser(id=1, nme='Darin') # nme is not a field (should be name)
        assert False, 'Expected AttributeError but got none'
    except AttributeError:
        pass

# ============ SQL Generation Tests ============

def test_connect() -> None:
    Model.connect(':memory:')
    assert Model._connection is not None
    Model._connection = None

# TODO
# def test_create_table() -> None:
#     ...

def test_create_table_sql_generation() -> None:
    point_sql_cmd = TestPoint._create_table_sql()
    assert point_sql_cmd == 'CREATE TABLE IF NOT EXISTS testpoint (name TEXT PRIMARY KEY NOT NULL, x INTEGER, y INTEGER)'

    user_sql_cmd = TestUser._create_table_sql()
    assert user_sql_cmd == 'CREATE TABLE IF NOT EXISTS testuser (id INTEGER PRIMARY KEY NOT NULL, name TEXT, age INTEGER, count INTEGER, note TEXT)'

def test_insert_sql_generation() -> None:
    point = TestPoint(name='A', x=1, y=2)
    sql_cmd, values = point._insert()
    assert sql_cmd == 'INSERT INTO testpoint (name, x, y) VALUES (?, ?, ?)'
    assert values == ('A', 1, 2)

    user = TestUser(id=1, name='Darin', age=21)
    sql_cmd, values = user._insert()
    assert sql_cmd == 'INSERT INTO testuser (id, name, age, count, note) VALUES (?, ?, ?, ?, ?)'
    assert values == (1, 'Darin', 21, 0, None)

def test_select_sql_generation() -> None:
    # select one
    point_sql_cmd, values = TestPoint._select('A')
    assert point_sql_cmd == 'SELECT name, x, y FROM testpoint WHERE name = ?'
    assert values == ('A',)

    user_sql_cmd, values = TestUser._select(1)
    assert user_sql_cmd == 'SELECT id, name, age, count, note FROM testuser WHERE id = ?'
    assert values == (1,)

    # select all
    point_sql_cmd, values = TestPoint._select_all()
    assert point_sql_cmd == 'SELECT name, x, y FROM testpoint'
    assert values == ()

    user_sql_cmd, values = TestUser._select_all()
    assert user_sql_cmd == 'SELECT id, name, age, count, note FROM testuser'
    assert values == ()

def test_update_sql_generation() -> None:
    ...

def test_delete_sql_generation() -> None:
    ...

# # Testing select single
# sql, params = User._select(1)
# print(sql)
# # SELECT id, name, age FROM user WHERE id = ?
# print(params)
# # (1,)

# # Testing select all
# sql, params = User._select_all()
# print(sql)
# # SELECT id, name, age FROM user
# print(params)
# # ()

# # Testing update
# u = User(id=1, name='Darin', age=21)
# sql, vals = u._update(age=22)
# print(sql)
# # UPDATE user SET age = ? WHERE id = ?
# print(vals)
# # (22, 1)

# sql, vals = u._update(name='David', age=23)
# print(sql)
# # UPDATE user SET name = ?, age = ? WHERE id = ?
# print(vals)
# # ('David', 23, 1)

# # sql, vals = u._update(name='David', age='invalid age')
# # TypeError: 'invalid age' does not match to the type INTEGER

# # Testing primary key requirement
# # class User(Model):
# #     id = IntegerField(primary_key=False)
# #     name = StringField(max_length=30, nullable=False)
# #     age = IntegerField(nullable=True)

# # u = User(id=1, name='Darin', age=21)
# # ValueError: 'user' requires at least one primary key

# # testing delete
# u = User(id=1, name='Darin', age=21)
# sql, vals = u._delete()
# print(sql)
# # DELETE FROM user WHERE id = ?
# print(vals)
# # (1,)

# # testing sqlite3 - creating table
# Model.connect(':memory:')

# class User(Model):
#     id = IntegerField(primary_key=True)
#     name = StringField(max_length=30)
# print(User._connection)
# User.create_table()

# cursor = Model._connection.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
# print(cursor.fetchall())

