from sqlalchemy.dialects.postgresql import insert

from app.db import SessionLocal
from app.models import Person


async def save_people(
    people: list[dict],
):

    if not people:
        print("No people to save")
        return

    async with SessionLocal() as session:

        stmt = insert(Person).values(people)

        stmt = stmt.on_conflict_do_nothing(
            index_elements=["id"]
        )

        result = await session.execute(stmt)

        await session.commit()

        saved_count = result.rowcount or 0

        print(f"Saved: {saved_count} characters")