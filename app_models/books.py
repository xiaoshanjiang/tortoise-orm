from tortoise import Model, fields


class Author(Model):
    name = fields.CharField(max_length=255)


class Book(Model):
    name = fields.CharField(max_length=255)
    author: fields.ForeignKeyRelation[Author] = fields.ForeignKeyField("models.Author", related_name="books")
    rating = fields.FloatField()
