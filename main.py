"""
This example shows how relations between models especially unique field work.

Key points in this example are use of ForeignKeyField and OneToOneField has to_field.
For other basic parts, it is the same as relation example.
"""
from tortoise import Tortoise, run_async

from app_models.employees import Employee


async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    root = await Employee.create(name="Root")
    loose = await Employee.create(name="Loose")
    _1 = await Employee.create(name="1. First H1", manager=root)
    _2 = await Employee.create(name="2. Second H1", manager=root)
    _1_1 = await Employee.create(name="1.1. First H2", manager=_1)
    _1_1_1 = await Employee.create(name="1.1.1. First H3", manager=_1_1)
    _2_1 = await Employee.create(name="2.1. Second H2", manager=_2)
    _2_2 = await Employee.create(name="2.2. Third H2", manager=_2)

    await _1.talks_to.add(_2, _1_1_1, loose)
    await _2_1.gets_talked_to.add(_2_2, _1_1, loose)

    # Evaluated off creation objects
    print(await loose.full_hierarchy__fetch_related())
    print(await root.full_hierarchy__async_for())
    print(await root.full_hierarchy__fetch_related())

    # Evaluated off new objects → Result is identical
    root2 = await Employee.get(name="Root")
    loose2 = await Employee.get(name="Loose")
    print(await loose2.full_hierarchy__fetch_related())
    print(await root2.full_hierarchy__async_for())
    print(await root2.full_hierarchy__fetch_related())


if __name__ == "__main__":
    run_async(run())