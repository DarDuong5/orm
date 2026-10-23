# Custom ORM (Object Relational Mapper)

## Overview

This is my implementation of an ORM (Object Relational Mapper) that allows custom Python objects to be represented as models. Instead of having to write SQL statements manually, we can use models with method calls to execute the SQL operations. Each **model** is mapped to a **table**. Then the **instances** of the models are mapped to **rows**. Each model has fields where each **field** is mapped to a **column**. Each field value passed as arguments in the instances is validated based on its data type and other constraints that exist. This means that any invalid data doesn't reach the database. The ORM supports basic SQLite operations such as insert, get, update, and delete, using parameterized queries to prevent SQL injection. 

## Architecture

The ORM is built using three layers:

**Fields (descriptors)**: Each field type (`IntegerField`, `StringField`) is a Python *descriptor* that manages a column's value on model instances -- validating the type and constraints (nullability, length) on an assignment and storing the value per-instance. Fields also carry SQL metadata (column type, primary key) used to generate the schema. 

**Models (metaclasses)**: A metaclass (`ModelMeta`) runs when a model class is defined: it scans the class for field descriptors, collects them, derives the table name, and enforces that each model has exactly one primary key. This is what turns a plain class declaration into a database-mapped model. 

**Persistence (methods)**: The `Model` base class provides the CRUD API (`save`, `get`, `get_all`, `update`, `delete`), and a SQL-generation layer that translates models into parameterized SQL statements, executed against SQLite.

## Usage
Requires Python 3.14+. No dependencies are required.

First, import all of the necessary modules:
```py
import fields
import model
```

Create your first model. In this case, I will make a pet model and go on from here. You can try with your own custom example.
```py
class PetModel(model.Model):
    pet_id: int = fields.IntegerField(primary_key=True, nullable=False)
    name: str = fields.StringField(max_length=30, default='')
    animal: str = fields.StringField(max_length=20, nullable=False)
```

Connect your model to SQLite.
```py
model.Model.connect(':memory:')
```

Create the table.
```py
PetModel.create_table()
```

Define an instance.
```py
quaker = PetModel(pet_id=1, name='Quaker', animal='Parrot')
```

To insert the instance into the table.
```py
quaker.save()
```

To select a row from the table.
```py
pet = PetModel.get(1)
```

To select all rows from the table.
```py
pets = PetModel.get_all()
```

To update the row.
```py
quaker.update(name='Bob')
```

To delete the row.
```py
quaker.delete()
```

To run tests, run `pytest unit_tests.py`

## Project Structure
```
fields.py # StringField and IntegerField are defined here.
model.py # ModelMeta, Model, and its methods are defined here.
unit_tests.py # All tests of the current features goes here.
```

**Note**: This is an ongoing personal project of mine, so more features will be added and `README.md` may be out of date. 

