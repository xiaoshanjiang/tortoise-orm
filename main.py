"""
This example demonstrates SQL Schema generation for each DB type supported.
"""
from tortoise import Tortoise, connections, fields, run_async
from tortoise.models import Model
from tortoise.utils import get_schema_sql

from models.sports import Event, Team, Tournament


async def run():
    print("SQLite:\n")
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    sql = get_schema_sql(connections.get("default"), safe=False)
    print(sql)

    print("\n\nMySQL:\n")
    await Tortoise.init(db_url="mysql://root:@127.0.0.1:3306/", modules={"models": ["__main__"]})
    sql = get_schema_sql(connections.get("default"), safe=False)
    print(sql)

    print("\n\nPostgreSQL:\n")
    await Tortoise.init(
        db_url="postgres://postgres:@127.0.0.1:5432/", modules={"models": ["__main__"]}
    )
    sql = get_schema_sql(connections.get("default"), safe=False)
    print(sql)


if __name__ == "__main__":
    run_async(run())
