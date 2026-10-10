from fields import Field, _MISSING

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

    # returns the query to create a table using explicit fields
    @classmethod
    def create_table(cls):
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

    @classmethod
    def get_table(cls):
        ...

    def save(self):
        ...

    def get(self):
        ...

    def update(self):
        ...

    def delete(self):
        ...
