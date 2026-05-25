import asyncio

import aiohttp

from app.loader import save_people
from app.swapi import (
    fetch_person,
    get_all_people_ids,
)

BATCH_SIZE = 10


async def process_batch(
    session: aiohttp.ClientSession,
    batch_ids: list[int],
):

    tasks = [
        fetch_person(session, person_id)
        for person_id in batch_ids
    ]

    results = await asyncio.gather(
        *tasks,
        return_exceptions=True,
    )

    people = [
        person
        for person in results
        if (
            person is not None
            and not isinstance(person, Exception)
        )
    ]

    if people:
        await save_people(people)

    print(
        f"Processed batch: "
        f"{len(people)} characters"
    )


async def main():

    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(
        timeout=timeout,
    ) as session:

        print("Loading character IDs...")

        person_ids = await get_all_people_ids(session)

        print(f"Found {len(person_ids)} characters")

        for i in range(0, len(person_ids), BATCH_SIZE):

            batch_ids = person_ids[i:i + BATCH_SIZE]

            print(
                f"Processing batch "
                f"{i // BATCH_SIZE + 1}"
            )

            await process_batch(
                session,
                batch_ids,
            )

        print("Done")


if __name__ == "__main__":
    asyncio.run(main())