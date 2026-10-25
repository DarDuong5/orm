from typing import Any

# means no default, value is required
# used instead of None because None maps to NULL in SQL
_MISSING = object()

# to represent an explicit field 
class Field:
    def __set_name__(self, owner, name) -> None:
        self.storage_name = name

    def __init__(self, primary_key=False, nullable=True, default=_MISSING) -> None:
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

    # handles default values
    def validate(self, value) -> None:
        # check if value is None and if the value is nullable
        if value is None:
            if self.nullable:
                return
            raise ValueError(f'{self.storage_name} is not nullable but got None')

        # if not, then move onto checking the type
        self._validate_type(value)

    # handles checking the type
    def _validate_type(self, value):
        ...

    # converts values from Python to Sqlite
    def to_db(self, value):
        return value

    # converts values from Sqlite to Python
    def from_db(self, value):
        return value

# to represent an integer field
class IntegerField(Field):
    sql_type = 'INTEGER'

    def __init__(self, primary_key=False, nullable=True, default=_MISSING) -> None:
        super().__init__(primary_key=primary_key, nullable=nullable, default=default)
            
    def _validate_type(self, value) -> None:
        if not isinstance(value, int):
            raise TypeError(f'{value!r} does not match to the type {self.sql_type}')   

# to represent a string field
class TextField(Field):
    sql_type = 'TEXT'

    def __init__(self, max_length=None, primary_key=False, nullable=True, default=_MISSING) -> None:
        super().__init__(primary_key=primary_key, nullable=nullable, default=default)
        self.max_length = max_length

    def _validate_type(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError(f'{value!r} does not match to the type {self.sql_type}')
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f'Length of value must be less than the given max_length:{self.max_length} given {value!r}')

# to represent a floating point field
class RealField(Field):
    sql_type = 'REAL'

    def __init__(self, precision=None, primary_key=False, nullable=True, default=_MISSING) -> None:
        super().__init__(primary_key=primary_key, nullable=nullable, default=default)
        self.precision = precision

    def _validate_type(self, value) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(f'{value!r} does not match to the type {self.sql_type}')

# to represent a boolean field
class BooleanField(Field):
    sql_type = 'BOOLEAN' # 0s or 1s

    def __init__(self, primary_key=False, nullable=True, default=_MISSING) -> None:
        super().__init__(primary_key=primary_key, nullable=nullable, default=default)

    def _validate_type(self, value):
        if not isinstance(value, bool):
            raise TypeError(f'{value!r} does not match to the type {self.sql_type}')

    def to_db(self, value) -> int | None:
        if value is None:
            return None
        
        return int(value)

    def from_db(self, value) -> bool | None:
        if value is None:
            return None

        return bool(value)
    
