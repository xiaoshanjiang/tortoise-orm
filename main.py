"""
This example shows some more complex querying

Key points are filtering by related names and using Q objects
"""
from tortoise import Tortoise, run_async
from tortoise.expressions import Q
from app_models.sports import Event, Team, Tournament


async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    tournament = Tournament(name="Tournament")
    await tournament.save()

    second_tournament = Tournament(name="Tournament 2")
    await second_tournament.save()

    event_first = Event(name="1", tournament=tournament)
    await event_first.save()
    event_second = await Event.create(name="2", tournament=second_tournament)
    await Event.create(name="3", tournament=tournament)
    await Event.create(name="4", tournament=second_tournament)

    await Event.filter(tournament=tournament)

    team_first = Team(name="First")
    await team_first.save()
    team_second = Team(name="Second")
    await team_second.save()

    await team_first.events.add(event_first)
    await event_second.participants.add(team_second)

    print(
        await Event.filter(Q(id__in=[event_first.id, event_second.id]) | Q(name="3"))
        .filter(participants__not=team_second.id)
        .order_by("tournament__id")
        .distinct()
    )

    print(await Team.filter(events__tournament_id=tournament.id).order_by("-events__name"))
    print(
        await Tournament.filter(events__name__in=["1", "3"])
        .order_by("-events__participants__name")
        .distinct()
    )

    print(await Team.filter(name__icontains="CON"))

    print(await Tournament.filter(events__participants__name__startswith="Fir"))
    print(await Tournament.filter(id__icontains=1).count())


if __name__ == "__main__":
    run_async(run())