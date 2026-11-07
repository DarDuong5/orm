from typing import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from model import Model

# Builder Pattern

# to represent a query
class Query:
    def __init__(self, model: Model) -> None:
        self.model = model # cls
        self.condition = None
        self.ordering = None
        self.limit_val = None

    def where(self, cond) -> Self:
        self.condition = cond
        return self

    def order_by(self, order) -> Self:
        self.ordering = order
        return self

    def limit(self, val) -> Self:
        self.limit_val = val
        return self

    # combines all of the sql statements and executes them 
    def execute_all(self) -> list[Model]:
        sql = f'SELECT {', '.join(self.model._fields.keys())} FROM {self.model._table_name}'
        params = ()

        if self.condition is not None:
            where_sql, where_params = self.condition._get_sql()
            sql += f' WHERE {where_sql}'
            params += where_params

        if self.ordering is not None:
            sql += f' ORDER BY {self.ordering}'

        if self.limit_val is not None:
            sql += f' LIMIT ?'
            params += (self.limit_val,)

        cursor = self.model._connection.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        return self.model._get_instances(rows)