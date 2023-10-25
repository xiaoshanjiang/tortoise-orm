"""
This example demonstrates most basic operations with single model
and a Table definition generation with comment support
"""
from tortoise import Tortoise, fields, run_async
from models.model import Event, Tournament, Team
from tortoise.query_utils import Prefetch


async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    tournament = await Tournament.create(name="tournament")
    await Event.create(name="First", tournament=tournament)
    await Event.create(name="Second", tournament=tournament)
    tournament_with_filtered = (
        await Tournament.all()
        .prefetch_related(Prefetch("events", queryset=Event.filter(name="First")))
        .first()
    )
    print(tournament_with_filtered)
    print(await Tournament.first().prefetch_related("events"))

    tournament_with_filtered_to_attr = (
        await Tournament.all()
        .prefetch_related(
            Prefetch(
                "events",
                queryset=Event.filter(name="First"),
                to_attr="to_attr_events_first",
            ),
            Prefetch(
                "events",
                queryset=Event.filter(name="Second"),
                to_attr="to_attr_events_second",
            ),
        )
        .first()
    )
    print(tournament_with_filtered_to_attr.to_attr_events_first)
    print(tournament_with_filtered_to_attr.to_attr_events_second)


if __name__ == "__main__":
    run_async(run())
