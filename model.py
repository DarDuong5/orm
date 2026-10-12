from typing import Any

from fields import Field, _MISSING

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

        return cls

# to represent a base model
class Model(metaclass=ModelMeta):
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

    # returns the data definition command to create a table
    @classmethod
    def _create_table(cls) -> str:
        columns = []
        for name, field in cls._fields.items():
            col = f'{name} {field.sql_type}'
            if field.primary_key:
                col += ' PRIMARY KEY'
            if not field.nullable:
                col += ' NOT NULL'
            columns.append(col)
        definitions = ', '.join(columns)
        return f'CREATE TABLE {cls._table_name} ({definitions})'

    # returns the data manipulation command to insert data 
    def _insert(self) -> SQLStatement:
        names = ', '.join(self._fields.keys())
        placeholders = ', '.join('?' for _ in self._fields)
        sql_cmd = f'INSERT INTO {self._table_name} ({names}) VALUES ({placeholders})'
        values = tuple(getattr(self, name) for name in self._fields)
        return sql_cmd, values

    def _save(self):
        ...

    # returns the data manipulation command to select data with primary key from a table
    @classmethod
    def _select(cls, primary_key) -> SQLStatement:
        columns = []
        primary = None

        # find primary key
        for name, field in cls._fields.items():
            if field.primary_key:
                primary = name
            columns.append(name)
        if primary is None:
            raise ValueError('No primary key')
        
        sql_cmd = f'SELECT {', '.join(columns)} FROM {cls._table_name} WHERE {primary} = ?'
        return sql_cmd, (primary_key, )

    # returns the data manipulation command to select all data from a table
    @classmethod
    def _select_all(cls) -> SQLStatement:
        sql_cmd = f'SELECT {', '.join(cls._fields.keys())} FROM {cls._table_name}'
        return sql_cmd, ()
       
    # returns the data manipulation command to update data from a table
    def _update(self, **fields) -> SQLStatement:
        # scan given fields to see if any are not actual fields
        for field in fields.keys():
            if field not in self._fields:
                raise ValueError(f'{field!r} is not a column in {self._table_name}')

        # find the primary key
        primary = None
        for name, field in self._fields.items():
            if field.primary_key:
                primary = name
        if primary is None:
            raise ValueError('No primary key')

        field_placeholders = ', '.join(f'{name} = ?' for name in fields)
        sql_cmd = f'UPDATE {self._table_name} SET {field_placeholders} WHERE {primary} = ?'
        primary_val = self.__dict__[primary]
        
        return sql_cmd, (*fields.values(), primary_val)

    # returns the data manipulation command to delete data from a table
    def _delete(self):
        ...

