from tortoise import Tortoise, fields
from tortoise.models import Model


class Tournament(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    def __str__(self):
        return self.name

    class Meta:
        app = "tournaments"


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    tournament_id = fields.IntField()
    # Here we make link to events.Team, not models.Team
    participants: fields.ManyToManyRelation["Team"] = fields.ManyToManyField(
        "events.Team", related_name="events", through="event_team"
    )

    def __str__(self):
        return self.name

    class Meta:
        app = "events"


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    event_team: fields.ManyToManyRelation[Event]

    def __str__(self):
        return self.name

    class Meta:
        app = "events"