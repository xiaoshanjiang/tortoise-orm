"""
This example demonstrates how you can use Tortoise if you have to
separate databases

Disclaimer: Although it allows to use two databases, you can't
use relations between two databases

Key notes of this example is using db_route for Tortoise init
and explicitly declaring model apps in class Meta
"""
from tortoise import Tortoise, connections, run_async
from tortoise.exceptions import OperationalError

from app_models.sports import Event, Team, Tournament   # pylint: disable=unused-import


async def run():
    """Corotine run"""
    await Tortoise.init(
        {
            "connections": {
                "first": {
                    "engine": "tortoise.backends.sqlite",
                    "credentials": {"file_path": "example.sqlite3"},
                },
                "second": {
                    "engine": "tortoise.backends.sqlite",
                    "credentials": {"file_path": "example1.sqlite3"},
                },
            },
            "apps": {
                "tournaments": {"models": ["__main__"], "default_connection": "first"},
                "events": {"models": ["__main__"], "default_connection": "second"},
            },
        }
    )
    await Tortoise.generate_schemas()
    client = connections.get("first")
    second_client = connections.get("second")

    tournament = await Tournament.create(name="Tournament")
    await Event(name="Event", tournament_id=tournament.id).save()

    try:
        await client.execute_query('SELECT * FROM "event"')
    except OperationalError:
        print("Expected it to fail")
    results = await second_client.execute_query('SELECT * FROM "event"')
    print(results)


if __name__ == "__main__":
    run_async(run())
