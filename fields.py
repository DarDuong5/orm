from typing import Any

# to represent an explicit field 
class Field:
    def __set_name__(self, owner, name) -> None:
        self.storage_name = name

    def __init__(self, primary_key=False, nullable=True, default=None) -> None:
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default

    def __get__(self, instance, owner) -> Any:
        if instance is None:
            return self
        return instance.__dict__[self.storage_name]

    def __set__(self, instance, value) -> None:
        self.validate(value)
        instance.__dict__[self.storage_name] = value

    def validate(self, value) -> None:
        ...

# to represent an integer field
class IntegerField(Field):
    sql_type = 'INTEGER'

    def __init__(self, primary_key=False, nullable=True, default=None) -> None:
        super().__init__(primary_key=primary_key, nullable=nullable, default=default)
            
    def validate(self, value) -> None:
        if not isinstance(value, int):
            raise TypeError(f'{value!r} does not match to the type {self.sql_type}')   

# to represent a string field
class StringField(Field):
    sql_type = 'TEXT'

    def __init__(self, max_length=None, primary_key=False, nullable=True, default=None) -> None:
        super().__init__(primary_key=primary_key, nullable=nullable, default=default)
        self.max_length = max_length

    def validate(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError(f'{value!r} does not match to the type {self.sql_type}')
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f'Length of value must be less than the given max_length:{self.max_length} given {value!r}')



