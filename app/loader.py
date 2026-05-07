from sqlalchemy import select

from app.db import SessionLocal
from app.models import Person


async def save_people(people: list[dict]):

    async with SessionLocal() as session:

        existing_ids_query = await session.execute(
            select(Person.id)
        )

        existing_ids = set(
            existing_ids_query.scalars().all()
        )

        new_people = []

        for person_data in people:

            if person_data["id"] in existing_ids:
                continue

            person = Person(**person_data)

            new_people.append(person)

        session.add_all(new_people)

        await session.commit()

        print(f"Saved: {len(new_people)} characters")