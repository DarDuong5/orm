from typing import Any, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from model import SQLStatement
    from fields import Field

# Composite Pattern

# to represent an expression
class Expression(ABC):
    def __and__(self, other) -> Compound:
        return Compound(self, 'AND', other)

    def __or__(self, other) -> Compound:
        return Compound(self, 'OR', other)

    # returns the sql statement for the expression
    @abstractmethod
    def _get_sql(self) -> SQLStatement:
        ...

# to represent a comparison expression
class Comparison(Expression):
    """Supports <, >, <=, >=, !=, =="""
    def __init__(self, field: Field, operator, value: Any): # field is the left operand, value is the right operand
        self.field = field
        self.operator = operator
        self.value = value

    def _get_sql(self) -> SQLStatement:
        sql_cmd = f'{self.field.storage_name} {self.operator} ?'
        params = (self.field.to_db(self.value),)
        return sql_cmd, params

    # ensure that the field type and the value type are the same
    def _validate(self) -> None:
        self.field._validate_type(self.value)

# to represent a compound expression
class Compound(Expression):
    """Supports AND and OR"""
    def __init__(self, left_exp: Expression, connector, right_exp: Expression):
        self.left_exp = left_exp
        self.connector = connector
        self.right_exp = right_exp

    def _get_sql(self) -> SQLStatement:
        left_sql, left_params = self.left_exp._get_sql()
        right_sql, right_params = self.right_exp._get_sql()
        sql_cmd = f'({left_sql}) {self.connector} ({right_sql})'
        params = left_params + right_params
        return sql_cmd, params

        