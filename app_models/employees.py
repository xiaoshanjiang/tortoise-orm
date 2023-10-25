from tortoise import Model, fields


class Employee(Model):
    name = fields.CharField(max_length=50)

    manager: fields.ForeignKeyNullableRelation["Employee"] = fields.ForeignKeyField(
        "models.Employee", related_name="team_members", null=True
    )
    team_members: fields.ReverseRelation["Employee"]

    talks_to: fields.ManyToManyRelation["Employee"] = fields.ManyToManyField(
        "models.Employee", related_name="gets_talked_to"
    )
    gets_talked_to: fields.ManyToManyRelation["Employee"]

    def __str__(self):
        return self.name

    async def full_hierarchy__async_for(self, level=0):
        """
        Demonstrates ``async for` to fetch relations

        An async iterator will fetch the relationship on-demand.
        """
        text = [
            "{}{} (to: {}) (from: {})".format(
                level * "  ",
                self,
                ", ".join([str(val) async for val in self.talks_to]),
                ", ".join([str(val) async for val in self.gets_talked_to]),
            )
        ]
        async for member in self.team_members:
            text.append(await member.full_hierarchy__async_for(level + 1))
        return "\n".join(text)

    async def full_hierarchy__fetch_related(self, level=0):
        """
        Demonstrates ``await .fetch_related`` to fetch relations

        On prefetching the data, the relationship files will contain a regular list.

        This is how one would get relations working on sync serialization/templating frameworks.
        """
        await self.fetch_related("team_members", "talks_to", "gets_talked_to")
        text = [
            "{}{} (to: {}) (from: {})".format(
                level * "  ",
                self,
                ", ".join([str(val) for val in self.talks_to]),
                ", ".join([str(val) for val in self.gets_talked_to]),
            )
        ]
        for member in self.team_members:
            text.append(await member.full_hierarchy__fetch_related(level + 1))
        return "\n".join(text)