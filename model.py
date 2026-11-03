from typing import Any, Self
import sqlite3

from fields import Field, _MISSING
from expressions import Expression

type SQLStatement = tuple[str, tuple[Any, ...]]

# to represent a model class factory (metaclass) 
class ModelMeta(type):
    def __new__(meta_cls, cls_name, bases, cls_dict) -> type:
        # used to store field instances
        fields_dict = {} 

        # scan class namespace for field instances
        for name, value in cls_dict.items():
            if isinstance(value, Field):
                fields_dict[name] = value 

        # create the class
        cls = super().__new__(meta_cls, cls_name, bases, cls_dict)

        # store the field dict on the class
        cls._fields = fields_dict
        # store table name
        cls._table_name = cls_name.lower()

        # ensure there's exactly one primary key (composite keys coming soon)
        if cls._fields:
            primary_keys = [name for name, field in cls._fields.items() if field.primary_key]
            if len(primary_keys) != 1:
                raise ValueError(f'{cls._table_name!r} requires at exactly one primary key given {len(primary_keys)}')
            
             # store the primary key
            cls._pk = primary_keys[0]

        return cls

# to represent a base model
class Model(metaclass=ModelMeta):
    _connection = None

    def __init__(self, **kwargs) -> None:
        # scan and check if every provided field exists
        for key in kwargs.keys():
            if key not in self._fields:
                raise AttributeError(f'{type(self).__name__!r} does not have a field named {key!r}')

        # scan the field dict
        for name, field in self._fields.items():
            # check if the field name is not provided and does not have a default value
            if name not in kwargs and field.default is _MISSING:
                raise ValueError(f'Missing required field {name!r}')
            # triggers the field descriptor's __set__, which enables validation and storage
            setattr(self, name, kwargs.get(name, field.default))

    # opens the connection and stores it
    @classmethod
    def connect(cls, db_path) -> None:
        cls._connection = sqlite3.connect(db_path)

    @classmethod
    def disconnect(cls) -> None:
        cls._connection.close()
        cls._connection = None

    # gets a cursor, executes, and commits to database
    @classmethod
    def create_table(cls) -> None:
        with cls._connection as conn:
            cursor = conn.cursor()
            cursor.execute(cls._create_table_sql())
            conn.commit()

    # returns the data definition command to create a table
    @classmethod
    def _create_table_sql(cls) -> str:
        columns = []
        for name, field in cls._fields.items():
            col = f'{name} {field.sql_type}'
            if field.primary_key:
                col += ' PRIMARY KEY'
            if not field.nullable:
                col += ' NOT NULL'
            columns.append(col)
        definitions = ', '.join(columns)
        return f'CREATE TABLE IF NOT EXISTS {cls._table_name} ({definitions})'

    # returns the data manipulation command to insert data 
    def _insert(self) -> SQLStatement:
        names = ', '.join(self._fields.keys())
        placeholders = ', '.join('?' for _ in self._fields)
        sql_cmd = f'INSERT INTO {self._table_name} ({names}) VALUES ({placeholders})'
        values = tuple(
            field.to_db(getattr(self, name)) 
            for name, field in self._fields.items()
        )

        return sql_cmd, values

    # saves the row in the database
    def save(self) -> None:
        sql_cmd, values = self._insert()
        cursor = self._connection.cursor()
        cursor.execute(sql_cmd, values)
        self._connection.commit()

    # returns the data manipulation command to select data with primary key from a table
    @classmethod
    def _select(cls, primary_key) -> SQLStatement:
        sql_cmd = f'SELECT {', '.join(cls._fields.keys())} FROM {cls._table_name} WHERE {cls._pk} = ?'
        return sql_cmd, (primary_key, )

    # gets the row from the table and creates the object and return it if it exists
    @classmethod
    def get(cls, primary_key) -> Self | None:
        sql_cmd, values = cls._select(primary_key)
        cursor = cls._connection.cursor()
        cursor.execute(sql_cmd, values)
        row = cursor.fetchone()

        if row is None:
            return

        kwargs = {
            name: field.from_db(value)
            for (name, field), value in zip(cls._fields.items(), row)
        }

        return cls(**kwargs)

    # returns the data manipulation command to select all data from a table
    @classmethod
    def _select_all(cls) -> SQLStatement:
        sql_cmd = f'SELECT {', '.join(cls._fields.keys())} FROM {cls._table_name}'
        return sql_cmd, ()

    # helper function for getting a list of instances
    @classmethod
    def _get_instances(cls, rows) -> list[Self]:
        instances = []
        for row in rows:
            kwargs = {}
            for name, value in zip(cls._fields.keys(), row):
                field = cls._fields[name]
                kwargs[name] = field.from_db(value)
            instances.append(cls(**kwargs))

        return instances

    # gets all of the rows in the table and creates and returns a list of instances of each one
    @classmethod
    def get_all(cls) -> list[Self]:
        sql_cmd, values = cls._select_all()
        cursor = cls._connection.cursor()
        cursor.execute(sql_cmd, values)
        rows = cursor.fetchall()
        return cls._get_instances(rows)
       
    # returns the data manipulation command to update data from a table
    def _update(self, **fields) -> SQLStatement:
        if not fields:
            raise ValueError('No fields provided to update')

        # scan given fields to see if any are not actual fields
        for field in fields.keys():
            if field not in self._fields:
                raise ValueError(f'{field!r} is not a column in {self._table_name}')

        # validate value before setting
        for name, value in fields.items():
            self._fields[name].validate(value)

        field_placeholders = ', '.join(f'{name} = ?' for name in fields)
        sql_cmd = f'UPDATE {self._table_name} SET {field_placeholders} WHERE {self._pk} = ?'
        primary_val = self._fields[self._pk].to_db(getattr(self, self._pk))
        values = [self._fields[name].to_db(value) for name, value in fields.items()]
        
        return sql_cmd, (*values, primary_val)

    # updates the row in the table 
    def update(self, **fields) -> None:
        sql_cmd, values = self._update(**fields)
        cursor = self._connection.cursor()
        cursor.execute(sql_cmd, values)
        self._connection.commit()

        # also update the attributes on self
        for name, value in fields.items():
            setattr(self, name, value) 

    # returns the data manipulation command to delete data from a table
    def _delete(self) -> SQLStatement:
        sql_cmd = f'DELETE FROM {self._table_name} WHERE {self._pk} = ?'
        return sql_cmd, (self.__dict__[self._pk], )

    # deletes the row in the table
    def delete(self) -> None:
        sql_cmd, values = self._delete()
        cursor = self._connection.cursor()
        cursor.execute(sql_cmd, values)
        self._connection.commit()

    # returns the clause command to filter data from a table
    @classmethod
    def _where(cls, exp: Expression) -> SQLStatement:
        select_all_sql, _, = cls._select_all()
        exp_sql_cmd, exp_value = exp._get_sql()
        sql_cmd = f'{select_all_sql} WHERE {exp_sql_cmd}'
        return sql_cmd, exp_value

    # filters rows in the table after selection
    @classmethod
    def where(cls, exp: Expression) -> list[Self]:
        sql_cmd, values = cls._where(exp)
        cursor = cls._connection.cursor()
        cursor.execute(sql_cmd, values)
        rows = cursor.fetchall()
        return cls._get_instances(rows)
