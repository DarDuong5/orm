from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from model import SQLStatement
    from fields import Field

# to represent an expression
class Expression:
    def __init__(self, field: Field, operator, value: Any): # field is the left operand, value is the right operand
        self.field = field
        self.operator = operator
        self.value = value

    # returns the sql statement for the expression
    def _get_sql(self) -> SQLStatement:
        sql_cmd = f'{self.field.storage_name} {self.operator} ?'
        params = (self.field.to_db(self.value),)
        return sql_cmd, params

    # ensure that the field type and the value type are the same
    def _validate(self) -> None:
        self.field._validate_type(self.value)

