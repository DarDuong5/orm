from fields import Field, IntegerField, StringField

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


    