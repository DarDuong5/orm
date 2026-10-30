import pytest

from fields import *
from fields import _MISSING
from model import *
from expressions import *

# ============ Test Classes ============

class Point(Model):
    name: str = TextField(max_length=10, primary_key=True, nullable=False)
    x: float = RealField(default=0)
    y: float = RealField(default=0)

class User(Model):
    id: int = IntegerField(primary_key=True, nullable=False)
    name: str = TextField(max_length=30)
    age: int = IntegerField()
    count: int = IntegerField(default=0)
    note: str = TextField(default=None)
    is_student: bool = BooleanField(default=False)

class Event(Model):
    id: int = IntegerField(primary_key=True, nullable=False)
    timestamp: datetime = DateTimeField(nullable=False)

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

    datetime_field = DateTimeField()
    assert isinstance(datetime_field, DateTimeField)

def test_primary_key() -> None:
    primary_int = IntegerField(primary_key=True)
    assert primary_int.primary_key is True

    not_primary_int = IntegerField()
    assert not_primary_int.primary_key is False

    primary_txt = TextField(primary_key=True)
    assert primary_txt.primary_key is True

    not_primary_txt = TextField()
    assert not_primary_txt.primary_key is False

    primary_real = RealField(primary_key=True)
    assert primary_real.primary_key is True

    not_primary_real = RealField()
    assert not_primary_real.primary_key is False

    primary_bool = BooleanField(primary_key=True)
    assert primary_bool.primary_key is True

    not_primary_bool = BooleanField()
    assert not_primary_bool.primary_key is False

    primary_datetime = DateTimeField(primary_key=True)
    assert primary_datetime.primary_key is True

    not_primary_datetime = DateTimeField()
    assert not_primary_datetime.primary_key is False

def test_nullable() -> None:
    nullable_int = IntegerField()
    assert nullable_int.nullable is True

    not_nullable_int = IntegerField(nullable=False)
    assert not_nullable_int.nullable is False

    nullable_txt = TextField()
    assert nullable_txt.nullable is True

    not_nullable_txt = TextField(nullable=False)
    assert not_nullable_txt.nullable is False

    nullable_real = RealField()
    assert nullable_real.nullable is True

    not_nullable_real = RealField(nullable=False)
    assert not_nullable_real.nullable is False

    nullable_bool = BooleanField()
    assert nullable_bool.nullable is True

    not_nullable_bool = BooleanField(nullable=False)
    assert not_nullable_bool.nullable is False

    nullable_datetime = DateTimeField()
    assert nullable_datetime.nullable is True

    not_nullable_datetime = DateTimeField(nullable=False)
    assert not_nullable_datetime.nullable is False

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

    default_datetime = DateTimeField(default=datetime(2026, 10, 25))
    assert default_datetime.default == datetime(2026, 10, 25)

    not_default_datetime = DateTimeField()
    assert not_default_datetime.default is _MISSING

def test_setters() -> None:
    point = Point.__new__(Point)
    point.name, point.x, point.y = 'A', 1, 2.4
    assert (point.name == 'A' and 
            point.x == 1.0 and 
            point.y == 2.4)

    user = User.__new__(User)
    user.id, user.name, user.age, user.count, user.note, user.is_student = 1, 'Darin', 21, 67, 'foo bar', True
    assert (user.id == 1 and 
            user.name == 'Darin' and 
            user.age == 21 and 
            user.count == 67 and 
            user.note == 'foo bar' 
            and user.is_student is True)

    event = Event.__new__(Event)
    event.id, event.timestamp = 1, datetime(2026, 10, 25, 6, 30, 15)
    assert event.id == 1 and event.timestamp == datetime(2026, 10, 25, 6, 30, 15)
    
def test_validate() -> None:
    point = Point.__new__(Point)
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

    user = User.__new__(User)
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

    event = Event.__new__(Event)
    # testing timestamp field type
    try:
        event.timestamp = 'Not a timestamp'
        assert False, 'Expected TypeError not none raised'
    except TypeError:
        pass
        
# ============ Model Tests ============

def test_model_attr() -> None:
    for field in Point._fields.values():
        assert isinstance(field, Field) is True

    for field in User._fields.values():
        assert isinstance(field, Field) is True

    for field in Event._fields.values():
        assert isinstance(field, Field) is True

    assert Point._table_name == 'point'
    assert User._table_name == 'user'
    assert Event._table_name == 'event'

    assert Point._pk == 'name'
    assert User._pk == 'id'
    assert Event._pk == 'id'

def test_base_model() -> None:
    point = Point(name='A', y=2.5)
    assert point.name == 'A'
    assert point.x == 0.0
    assert point.y == 2.5

    user = User(id=1, name='Darin', age=21)
    assert user.id == 1
    assert user.name == 'Darin'
    assert user.age == 21
    assert user.count == 0
    assert user.note is None
    assert user.is_student is False

    event = Event(id=1, timestamp=datetime(2026, 10, 25, 6, 30, 15))
    assert event.id == 1
    assert event.timestamp == datetime(2026, 10, 25, 6, 30, 15)

def test_base_model_validation() -> None:
    try:
        Point(name='Name too long') # provided string value exceeds the max length of string field
        assert False, 'Expected ValueError but got none'
    except ValueError:
        pass

    try:
        Point(name=10) # invalid type (name should be str)
        assert False, 'Expected ValueError but got none'
    except TypeError:
        pass

    try:
        User(id='invalid type', name='Darin') # invalid type (id should be int)
        assert False, 'Expected TypeError but got none'
    except TypeError:
        pass

    try:
        User(id=1, nme='Darin') # nme is not a field (should be name)
        assert False, 'Expected AttributeError but got none'
    except AttributeError:
        pass

# ============ SQL Generation Tests ============

def test_create_table_sql_generation() -> None:
    point_sql_cmd = Point._create_table_sql()
    assert point_sql_cmd == 'CREATE TABLE IF NOT EXISTS point (name TEXT PRIMARY KEY NOT NULL, x REAL, y REAL)'

    user_sql_cmd = User._create_table_sql()
    assert user_sql_cmd == 'CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY NOT NULL, name TEXT, age INTEGER, count INTEGER, note TEXT, is_student BOOLEAN)'

    event_sql_cmd = Event._create_table_sql()
    assert event_sql_cmd == 'CREATE TABLE IF NOT EXISTS event (id INTEGER PRIMARY KEY NOT NULL, timestamp DATETIME NOT NULL)'

def test_insert_sql_generation() -> None:
    point = Point(name='A', x=1, y=2.5)
    sql_cmd, values = point._insert()
    assert sql_cmd == 'INSERT INTO point (name, x, y) VALUES (?, ?, ?)'
    assert values == ('A', 1.0, 2.5)

    user = User(id=1, name='Darin', age=21)
    sql_cmd, values = user._insert()
    assert sql_cmd == 'INSERT INTO user (id, name, age, count, note, is_student) VALUES (?, ?, ?, ?, ?, ?)'
    assert values == (1, 'Darin', 21, 0, None, 0)

    event = Event(id=1, timestamp=datetime(2026, 10, 25, 6, 30, 15))
    sql_cmd, values = event._insert()
    assert sql_cmd == 'INSERT INTO event (id, timestamp) VALUES (?, ?)'
    assert values == (1, '2026-10-25T06:30:15')

def test_select_sql_generation() -> None:
    # select one
    point_sql_cmd, values = Point._select('A')
    assert point_sql_cmd == 'SELECT name, x, y FROM point WHERE name = ?'
    assert values == ('A',)

    user_sql_cmd, values = User._select(1)
    assert user_sql_cmd == 'SELECT id, name, age, count, note, is_student FROM user WHERE id = ?'
    assert values == (1,)

    event_sql_cmd, values = Event._select(1)
    assert event_sql_cmd == 'SELECT id, timestamp FROM event WHERE id = ?'
    assert values == (1,)

    # select all
    point_sql_cmd, values = Point._select_all()
    assert point_sql_cmd == 'SELECT name, x, y FROM point'
    assert values == ()

    user_sql_cmd, values = User._select_all()
    assert user_sql_cmd == 'SELECT id, name, age, count, note, is_student FROM user'
    assert values == ()

    event_sql_cmd, values = Event._select_all()
    assert event_sql_cmd == 'SELECT id, timestamp FROM event'
    assert values == ()    

def test_update_sql_generation() -> None:
    point = Point(name='A', x=1, y=2)
    point_sql_cmd, values = point._update(name='B', x=2)
    assert point_sql_cmd == 'UPDATE point SET name = ?, x = ? WHERE name = ?'
    assert values == ('B', 2, 'A')

    user = User(id=1, name='Darin', age=21)
    user_sql_cmd, values = user._update(note='likes space')
    assert user_sql_cmd == 'UPDATE user SET note = ? WHERE id = ?'
    assert values == ('likes space', 1)

    event = Event(id=1, timestamp=datetime(2026, 10, 25, 6, 30, 15))
    sql_cmd, values = event._update(timestamp=datetime(2027, 1, 1))
    assert sql_cmd == 'UPDATE event SET timestamp = ? WHERE id = ?'
    assert values == ('2027-01-01T00:00:00', 1)

    # invalid fields
    try:
        point._update(nonexistent_key='I do not exist')
        assert False, 'Expected ValueError but got none'
    except ValueError:
        pass

    try:
        user._update(nonexistent_key='I do not exist')
        assert False, 'Expected ValueError but got none'
    except ValueError:
        pass

    try:
        event._update(nonexistent_key='I do no exist')
        assert False, 'Expected ValueError but got none'
    except ValueError:
        pass

    # invalid types
    try:
        point._update(x='I am an int, not a string!')
        assert False, 'Expected TypeError but got none'
    except TypeError:
        pass

    try:
        user._update(age='I am an int, not a string!')
        assert False, 'Expected TypeError but got none'
    except TypeError:
        pass

    try: 
        event.update(timestamp='I am a datetime, not a string!')
        assert False, 'Expected TypeError but got none'
    except TypeError:
        pass

    # no fields passed in
    try:
        point._update()
        assert False, 'Expected ValueError but got none'
    except ValueError:
        pass

    try:
        user._update()
        assert False, 'Expected ValueError but got none'
    except ValueError:
        pass

    try:
        event._update()
        assert False, 'Expected ValueError but got none'
    except ValueError:
        pass

def test_delete_sql_generation() -> None:
    point = Point(name='A', x=1, y=2.5)
    point_sql_cmd, values = point._delete()
    assert point_sql_cmd == 'DELETE FROM point WHERE name = ?'
    assert values == ('A',)

    user = User(id=1, name='Darin', age=21)
    user_sql_cmd, values = user._delete()
    assert user_sql_cmd == 'DELETE FROM user WHERE id = ?'
    assert values == (1,)

    event = Event(id=1, timestamp=datetime(2026, 10, 25, 6, 30, 15))
    sql_cmd, values = event._delete()
    assert sql_cmd == 'DELETE FROM event WHERE id = ?'
    assert values == (1,)

# ============ SQL API Tests ============

@pytest.fixture
def db():
    Model.connect(':memory:')
    Point.create_table()
    User.create_table()
    Event.create_table()
    yield
    Model._connection.close()
    Model._connection = None

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

def test_create_table(db) -> None:
    cursor = Model._connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    assert ('point',) in tables
    assert ('user',) in tables
    assert ('event',) in tables

def test_save(db) -> None:
    Point(name='A', x=1, y=2.5).save()
    User(id=1, name='Darin', age=21).save()
    Event(id=1, timestamp=datetime(2026, 10, 25, 6, 30, 15)).save()

    # verify the row is in the database
    cursor = Model._connection.cursor()
    cursor.execute("SELECT name, x, y FROM point WHERE name = 'A'")
    row = cursor.fetchone()
    assert row == ('A', 1.0, 2.5)

    cursor.execute('SELECT id, name, age FROM user WHERE id = 1')
    row = cursor.fetchone()
    assert row == (1, 'Darin', 21)

    cursor.execute('SELECT id, timestamp FROM event WHERE id = 1')
    row = cursor.fetchone()
    assert row == (1, '2026-10-25T06:30:15')

def test_get(db) -> None:
    Point(name='A', x=1.0, y=2.5).save()
    User(id=1, name='Darin', age=21).save()
    Event(id=1, timestamp=datetime(2026, 10, 25, 6, 30, 15)).save()

    point = Point.get('A')
    user = User.get(1)
    event = Event.get(1)

    assert isinstance(point, Point)
    assert point.name == 'A' and point.x == 1.0 and point.y == 2.5
    assert isinstance(user, User)
    assert user.id == 1 and user.name == 'Darin' and user.age == 21
    assert isinstance(event, Event)
    assert event.id == 1 and event.timestamp == datetime(2026, 10, 25, 6, 30, 15)

def test_get_all(db) -> None:
    Point(name='A').save()
    Point(name='B', x=1.0, y=2.5).save()
    Point(name='C', x=1.7, y=2).save()

    points = Point.get_all()
    assert all(isinstance(point, Point) for point in points)
    assert points[0].name == 'A' and points[0].x == 0.0 and points[0].y == 0.0
    assert points[1].name == 'B' and points[1].x == 1.0 and points[1].y == 2.5
    assert points[2].name == 'C' and points[2].x == 1.7 and points[2].y == 2.0

    User(id=1, name='Darin', age=21).save()
    User(id=2, name='John', age=22).save()
    User(id=3, name='Jane', age=23).save()

    users = User.get_all()
    assert all(isinstance(user, User) for user in users)
    assert users[0].id == 1 and users[0].name == 'Darin' and users[0].age == 21
    assert users[1].id == 2 and users[1].name == 'John' and users[1].age == 22
    assert users[2].id == 3 and users[2].name == 'Jane' and users[2].age == 23

    Event(id=1, timestamp=datetime(2026, 10, 25, 6, 30, 15)).save()
    Event(id=2, timestamp=datetime(2026, 10, 25, 7, 45, 20)).save()
    Event(id=3, timestamp=datetime(2026, 10, 25, 9, 00, 25)).save()

    events = Event.get_all()
    assert all(isinstance(event, Event) for event in events)
    assert events[0].id == 1 and events[0].timestamp == datetime(2026, 10, 25, 6, 30, 15)
    assert events[1].id == 2 and events[1].timestamp == datetime(2026, 10, 25, 7, 45, 20)
    assert events[2].id == 3 and events[2].timestamp == datetime(2026, 10, 25, 9, 00, 25)

def test_update(db) -> None:
    point = Point(name='A', x=1.25, y=2.5)
    point.save()
    point.update(x=0.0)
    updated_point = Point.get('A')
    assert (updated_point.name == 'A' and
            updated_point.x == 0.0 and
            updated_point.y == 2.5)

    user = User(id=1, name='Darin', age=21)
    user.save()
    user.update(name='Bob', age=22, count=5, note='Bob the builder', is_student=True)
    updated_user = User.get(1)
    assert (updated_user.id == 1 and 
            updated_user.name == 'Bob' and 
            updated_user.age == 22 and
            updated_user.count == 5 and
            updated_user.note == 'Bob the builder' and
            updated_user.is_student is True)

    event = Event(id=1, timestamp=datetime(2026, 10, 25, 6, 30, 15))
    event.save()
    event.update(timestamp=datetime(2027, 1, 1))
    updated_event = Event.get(1)
    assert updated_event.id == 1 and updated_event.timestamp == datetime(2027, 1, 1)

def test_delete(db) -> None:
    Point(name='A').save()
    User(id=1, name='Darin', age=21).save()
    Event(id=1, timestamp=datetime(2026, 10, 25, 6, 30, 15)).save()

    point = Point.get('A')
    assert point.name == 'A' and point.x == 0.0 and point.y == 0.0
    user = User.get(1)
    assert user.id == 1 and user.name == 'Darin' and user.age == 21
    event = Event.get(1)
    assert event.id == 1 and event.timestamp == datetime(2026, 10, 25, 6, 30, 15)

    point.delete()
    user.delete()
    event.delete()
    point = Point.get('A')
    user = User.get(1)
    event = Event.get(1)
    assert point is None
    assert user is None
    assert event is None

# ============ Expression Tests ============
def test_exp_cmd() -> None:
    exp = Expression(field=User.age, operator='=', value=21)
    sql_cmd, params = exp._get_sql()
    assert sql_cmd == 'age = ?'
    assert params == (21, )

def test_exp_validate() -> None:
    # valid type check
    try:
        exp = Expression(field=User.age, operator='=', value=21)
        exp._validate()
        assert True
    except TypeError:
        assert False, 'Did not expect TypeError but got one'

    # invalid type check
    try:
        exp = Expression(field=User.age, operator='=', value='Not an int')
        exp._validate()
        assert False, 'Expected TypeError but got none'
    except TypeError:
        pass

# ============ Field Expression Tests ============
def test_gt() -> None:
    user_exp = User.age > 21
    assert isinstance(user_exp, Expression)
    sql_cmd_user, params_user = user_exp._get_sql()
    assert sql_cmd_user == 'age > ?'
    assert params_user == (21,)

    point_exp = Point.x > 1.75
    assert isinstance(point_exp, Expression)
    sql_cmd_point, params_point = point_exp._get_sql()
    assert sql_cmd_point == 'x > ?'
    assert params_point == (1.75,)

def test_lt() -> None:
    user_exp = User.age < 21
    assert isinstance(user_exp, Expression)
    sql_cmd_user, params_user = user_exp._get_sql()
    assert sql_cmd_user == 'age < ?'
    assert params_user == (21,)

    point_exp = Point.x < 1.75
    assert isinstance(point_exp, Expression)
    sql_cmd_point, params_point = point_exp._get_sql()
    assert sql_cmd_point == 'x < ?'
    assert params_point == (1.75,)

def test_ge() -> None:
    user_exp = User.age >= 21
    assert isinstance(user_exp, Expression)
    sql_cmd_user, params_user = user_exp._get_sql()
    assert sql_cmd_user == 'age >= ?'
    assert params_user == (21,)

    point_exp = Point.x >= 1.75
    assert isinstance(point_exp, Expression)
    sql_cmd_point, params_point = point_exp._get_sql()
    assert sql_cmd_point == 'x >= ?'
    assert params_point == (1.75,)

def test_le() -> None:
    user_exp = User.age <= 21
    assert isinstance(user_exp, Expression)
    sql_cmd_user, params_user = user_exp._get_sql()
    assert sql_cmd_user == 'age <= ?'
    assert params_user == (21,)

    point_exp = Point.x <= 1.75
    assert isinstance(point_exp, Expression)
    sql_cmd_point, params_point = point_exp._get_sql()
    assert sql_cmd_point == 'x <= ?'
    assert params_point == (1.75,)

def test_eq() -> None:
    user_exp = User.name == 'Darin'
    assert isinstance(user_exp, Expression)
    sql_cmd_user, params_user = user_exp._get_sql()
    assert sql_cmd_user == 'name = ?'
    assert params_user == ('Darin',)

    point_exp = Point.name == 'A'
    assert isinstance(point_exp, Expression)
    sql_cmd_point, params_point = point_exp._get_sql()
    assert sql_cmd_point == 'name = ?'
    assert params_point == ('A',)

def test_ne() -> None:
    user_exp = User.age != 21
    assert isinstance(user_exp, Expression)
    sql_cmd_user, params_user = user_exp._get_sql()
    assert sql_cmd_user == 'age != ?'
    assert params_user == (21,)

    point_exp = Point.x != 1.75
    assert isinstance(point_exp, Expression)
    sql_cmd_point, params_point = point_exp._get_sql()
    assert sql_cmd_point == 'x != ?'
    assert params_point == (1.75,)

    
