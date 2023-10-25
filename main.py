"""
This example demonstrates most basic operations with single model
and a Table definition generation with comment support
"""
from tortoise import Tortoise, run_async
from tortoise.exceptions import OperationalError
from tortoise.transactions import atomic, in_transaction
from models.model import Event


async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    try:
        async with in_transaction() as connection:
            event = Event(name="Test")
            await event.save(using_db=connection)
            await Event.filter(id=event.id).using_db(connection).update(name="Updated name")
            saved_event = await Event.filter(name="Updated name").using_db(connection).first()
            await connection.execute_query("SELECT * FROM non_existent_table")
    except OperationalError as ex:
        print(ex)
    saved_event = await Event.filter(name="Updated name").first()
    print(saved_event)

    @atomic()
    async def bound_to_fall():
        event = await Event.create(name="Test")
        await Event.filter(id=event.id).update(name="Updated name")
        saved_event = await Event.filter(name="Updated name").first()
        print(saved_event.name)
        raise OperationalError('opps! something went wrong.')

    try:
        await bound_to_fall()
    except OperationalError as ex:
        print(ex)
    saved_event = await Event.filter(name="Updated name").first()
    print(saved_event)


if __name__ == "__main__":
    run_async(run())
