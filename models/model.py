from tortoise import fields
from tortoise.models import Model


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField(description="Name of the event that corresponds to an action")
    datetime = fields.DatetimeField(
        null=True, description="Datetime of when the event was generated"
    )

    class Meta:
        table = "event"
        table_description = "This table contains a list of all the example events"

    def __str__(self):
        return self.name