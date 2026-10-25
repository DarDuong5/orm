from fields import *
from fields import _MISSING
from model import *

# ============ Test Classes ============

class TestPoint(Model):
    name: str = TextField(max_length=10, primary_key=True, nullable=False)
    x: float = RealField(default=0)
    y: float = RealField(default=0)

class TestUser(Model):
    id: int = IntegerField(primary_key=True, nullable=False)
    name: str = TextField(max_length=30)
    age: int = IntegerField()
    count: int = IntegerField(default=0)
    note: str = TextField(default=None)
    is_student: bool = BooleanField(default=False)

# ============ Field Tests ============

def test_field_types() -> None:
    string_field = TextField()
    assert isinstance(string_field, TextField)

    integer_field = IntegerField()
    assert isinstance(integer_field, IntegerField)

    float_field = RealField()
    assert isinstance(float_field, RealField)

    bool_field = BooleanField()
    assert isinstance(bool_field, BooleanField)

def test_primary_key() -> None:
    primary_int = IntegerField(primary_key=True)
    assert primary_int.primary_key == True

    not_primary_int = IntegerField()
    assert not_primary_int.primary_key == False

    primary_txt = TextField(primary_key=True)
    assert primary_txt.primary_key == True

    not_primary_txt = TextField()
    assert not_primary_txt.primary_key == False

    primary_real = RealField(primary_key=True)
    assert primary_real.primary_key == True

    not_primary_real = RealField()
    assert not_primary_real.primary_key == False

    primary_bool = BooleanField(primary_key=True)
    assert primary_bool.primary_key == True

    not_primary_bool = BooleanField()
    assert not_primary_bool.primary_key == False

def test_nullable() -> None:
    nullable_int = IntegerField()
    assert nullable_int.nullable == True

    not_nullable_int = IntegerField(nullable=False)
    assert not_nullable_int.nullable == False

    nullable_txt = TextField()
    assert nullable_txt.nullable == True

    not_nullable_txt = TextField(nullable=False)
    assert not_nullable_txt.nullable == False

    nullable_real = RealField()
    assert nullable_real.nullable == True

    not_nullable_real = RealField(nullable=False)
    assert not_nullable_real.nullable == False

    nullable_bool = BooleanField()
    assert nullable_bool.nullable == True

    not_nullable_bool = BooleanField(nullable=False)
    assert not_nullable_bool.nullable == False

def test_default() -> None:
    default_int = IntegerField(default=1)
    assert default_int.default == 1

    not_default_int = IntegerField()
    assert not_default_int.default is _MISSING

    default_txt = TextField(default='')
    assert default_txt.default == ''

    not_default_txt = TextField()
    assert not_default_txt.default is _MISSING

    default_real = RealField(default=1.0)
    assert default_real.default == 1.0

    not_default_real = RealField()
    assert not_default_real.default is _MISSING  

    default_bool = BooleanField(default=True)
    assert default_bool.default is True

    not_default_bool = BooleanField()
    assert not_default_bool.default is _MISSING  

def test_setters() -> None:
    point = TestPoint.__new__(TestPoint)
    point.name, point.x, point.y = 'A', 1, 2.4
    assert (point.name == 'A' and 
            point.x == 1.0 and 
            point.y == 2.4)

    user = TestUser.__new__(TestUser)
    user.id, user.name, user.age, user.count, user.note, user.is_student = 1, 'Darin', 21, 67, 'foo bar', True
    assert (user.id == 1 and 
            user.name == 'Darin' and 
            user.age == 21 and 
            user.count == 67 and 
            user.note == 'foo bar' 
            and user.is_student is True)

def test_validate() -> None:
    point = TestPoint.__new__(TestPoint)
    # testing text and real field types
    try: 
        point.name = "Name is too long"
        assert False, 'Expected ValueError but none raised'
    except ValueError:
        pass

    try:
        point.x = "Not a real"
        assert False, 'Expected TypeError but none raised'
    except TypeError:
        pass

    try:
        point.y = "Also not a real"
        assert False, 'Expected TypeError but none raised'
    except TypeError:
        pass

    user = TestUser.__new__(TestUser)
    # testing integer and boolean field types
    try:
        user.age = 'Not an integer'
        assert False, 'Expected TypeError but none raised'
    except TypeError:
        pass

    try:
        user.is_student = 'Not a boolean'
        assert False, 'Expected TypeError but none raised'
    except TypeError:
        pass
        
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
    point = TestPoint(name='A', y=2.5)
    assert point.name == 'A'
    assert point.x == 0.0
    assert point.y == 2.5

    user = TestUser(id=1, name='Darin', age=21)
    assert user.id == 1
    assert user.name == 'Darin'
    assert user.age == 21
    assert user.count == 0
    assert user.note is None
    assert user.is_student is False

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

def test_create_table_sql_generation() -> None:
    point_sql_cmd = TestPoint._create_table_sql()
    assert point_sql_cmd == 'CREATE TABLE IF NOT EXISTS testpoint (name TEXT PRIMARY KEY NOT NULL, x REAL, y REAL)'

    user_sql_cmd = TestUser._create_table_sql()
    assert user_sql_cmd == 'CREATE TABLE IF NOT EXISTS testuser (id INTEGER PRIMARY KEY NOT NULL, name TEXT, age INTEGER, count INTEGER, note TEXT, is_student BOOLEAN)'

def test_insert_sql_generation() -> None:
    point = TestPoint(name='A', x=1, y=2.5)
    sql_cmd, values = point._insert()
    assert sql_cmd == 'INSERT INTO testpoint (name, x, y) VALUES (?, ?, ?)'
    assert values == ('A', 1.0, 2.5)

    user = TestUser(id=1, name='Darin', age=21)
    sql_cmd, values = user._insert()
    assert sql_cmd == 'INSERT INTO testuser (id, name, age, count, note, is_student) VALUES (?, ?, ?, ?, ?, ?)'
    assert values == (1, 'Darin', 21, 0, None, False)

def test_select_sql_generation() -> None:
    # select one
    point_sql_cmd, values = TestPoint._select('A')
    assert point_sql_cmd == 'SELECT name, x, y FROM testpoint WHERE name = ?'
    assert values == ('A',)

    user_sql_cmd, values = TestUser._select(1)
    assert user_sql_cmd == 'SELECT id, name, age, count, note, is_student FROM testuser WHERE id = ?'
    assert values == (1,)

    # select all
    point_sql_cmd, values = TestPoint._select_all()
    assert point_sql_cmd == 'SELECT name, x, y FROM testpoint'
    assert values == ()

    user_sql_cmd, values = TestUser._select_all()
    assert user_sql_cmd == 'SELECT id, name, age, count, note, is_student FROM testuser'
    assert values == ()

def test_update_sql_generation() -> None:
    point = TestPoint(name='A', x=1, y=2)
    point_sql_cmd, values = point._update(name='B', x=2)
    assert point_sql_cmd == 'UPDATE testpoint SET name = ?, x = ? WHERE name = ?'
    assert values == ('B', 2, 'A')

    user = TestUser(id=1, name='Darin', age=21)
    user_sql_cmd, values = user._update(note='likes space')
    assert user_sql_cmd == 'UPDATE testuser SET note = ? WHERE id = ?'
    assert values == ('likes space', 1)

    # invalid fields
    try:
        point_sql_cmd, values = point._update(nonexistent_key='I do not exist')
        assert False, 'Expected ValueError but got none'
    except ValueError:
        pass

    try:
        user_sql_cmd, values = user._update(nonexistent_key='I do not exist')
        assert False, 'Expected ValueError but got none'
    except ValueError:
        pass

    # invalid types
    try:
        point_sql_cmd, values = point._update(x='I am an int, not a string!')
        assert False, 'Expected TypeError but got none'
    except TypeError:
        pass

    try:
        user_sql_cmd, values = user._update(age='I am an int, not a string!')
        assert False, 'Expected TypeError but got none'
    except TypeError:
        pass

    # no fields passed in
    try:
        point_sql_cmd, values = point._update()
        assert False, 'Expected ValueError but got none'
    except ValueError:
        pass

    try:
        user_sql_cmd, values = user._update()
        assert False, 'Expected ValueError but got none'
    except ValueError:
        pass

def test_delete_sql_generation() -> None:
    point = TestPoint(name='A', x=1, y=2.5)
    point_sql_cmd, values = point._delete()
    assert point_sql_cmd == 'DELETE FROM testpoint WHERE name = ?'
    assert values == ('A',)

    user = TestUser(id=1, name='Darin', age=21)
    user_sql_cmd, values = user._delete()
    assert user_sql_cmd == 'DELETE FROM testuser WHERE id = ?'
    assert values == (1,)

# ============ SQL API Tests ============

def test_connect() -> None:
    Model.connect(':memory:')
    assert Model._connection is not None
    Model._connection.close()
    Model._connection = None

def test_disconnect() -> None:
    Model.connect(':memory:')
    assert Model._connection is not None
    Model.disconnect()
    assert Model._connection is None

def test_create_table() -> None:
    Model.connect(':memory:')
    TestPoint.create_table()
    TestUser.create_table()

    cursor = Model._connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    assert ('testpoint',) in tables
    assert ('testuser',) in tables

    Model._connection.close()
    Model._connection = None

def test_save() -> None:
    Model.connect(':memory:')
    TestPoint.create_table()
    TestUser.create_table()

    point = TestPoint(name='A', x=1, y=2.5)
    point.save()
    user = TestUser(id=1, name='Darin', age=21)
    user.save()

    # verify the row is in the database
    cursor = Model._connection.cursor()
    cursor.execute("SELECT name, x, y FROM testpoint WHERE name = 'A'")
    row = cursor.fetchone()
    assert row == ('A', 1.0, 2.5)

    cursor.execute('SELECT id, name, age FROM testuser WHERE id = 1')
    row = cursor.fetchone()
    assert row == (1, 'Darin', 21)

    Model._connection.close()
    Model._connection = None

def test_get() -> None:
    Model.connect(':memory:')
    TestPoint.create_table()
    TestUser.create_table()
    TestPoint(name='A', x=1.0, y=2.5).save()
    TestUser(id=1, name='Darin', age=21).save()

    point = TestPoint.get('A')
    user = TestUser.get(1)

    assert isinstance(point, TestPoint)
    assert point.name == 'A' and point.x == 1.0 and point.y == 2.5
    assert isinstance(user, TestUser)
    assert user.id == 1 and user.name == 'Darin' and user.age == 21

    Model._connection.close()
    Model._connection = None

def test_get_all() -> None:
    Model.connect(':memory:')
    TestPoint.create_table()
    TestUser.create_table()

    TestPoint(name='A').save()
    TestPoint(name='B', x=1.0, y=2.5).save()
    TestPoint(name='C', x=1.7, y=2).save()

    points = TestPoint.get_all()
    assert all(isinstance(point, TestPoint) for point in points)
    assert points[0].name == 'A' and points[0].x == 0.0 and points[0].y == 0.0
    assert points[1].name == 'B' and points[1].x == 1.0 and points[1].y == 2.5
    assert points[2].name == 'C' and points[2].x == 1.7 and points[2].y == 2.0

    TestUser(id=1, name='Darin', age=21).save()
    TestUser(id=2, name='John', age=22).save()
    TestUser(id=3, name='Jane', age=23).save()

    users = TestUser.get_all()
    assert all(isinstance(user, TestUser) for user in users)
    assert users[0].id == 1 and users[0].name == 'Darin' and users[0].age == 21
    assert users[1].id == 2 and users[1].name == 'John' and users[1].age == 22
    assert users[2].id == 3 and users[2].name == 'Jane' and users[2].age == 23

    Model._connection.close()
    Model._connection = None

def test_update() -> None:
    Model.connect(':memory:')
    TestPoint.create_table()
    TestUser.create_table()

    point = TestPoint(name='A', x=1.25, y=2.5)
    point.save()
    point.update(x=0.0)
    updated_point = TestPoint.get('A')
    assert (updated_point.name == 'A' and
            updated_point.x == 0.0 and
            updated_point.y == 2.5)

    user = TestUser(id=1, name='Darin', age=21)
    user.save()
    user.update(name='Bob', age=22, count=5, note='Bob the builder', is_student=True)
    updated_user = TestUser.get(1)
    assert (updated_user.id == 1 and 
            updated_user.name == 'Bob' and 
            updated_user.age == 22 and
            updated_user.count == 5 and
            updated_user.note == 'Bob the builder' and
            updated_user.is_student == True)
    
    Model._connection.close()
    Model._connection = None

def test_delete() -> None:
    Model.connect(':memory:')
    TestPoint.create_table()
    TestUser.create_table()
    TestPoint(name='A').save()
    TestUser(id=1, name='Darin', age=21).save()

    point = TestPoint.get('A')
    assert point.name == 'A' and point.x == 0.0 and point.y == 0.0
    user = TestUser.get(1)
    assert user.id == 1 and user.name == 'Darin' and user.age == 21

    point.delete()
    user.delete()
    point = TestPoint.get('A')
    user = TestUser.get(1)
    assert point is None
    assert user is None
    
    Model._connection.close()
    Model._connection = None