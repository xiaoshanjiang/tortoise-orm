from tortoise import fields
from tortoise.models import Model

class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    class Meta:
        table = "event"

    def __str__(self):
        return self.name
