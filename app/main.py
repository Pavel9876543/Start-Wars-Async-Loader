import asyncio

import aiohttp

from app.loader import save_people
from app.swapi import fetch_person


async def main():

    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(
        timeout=timeout,
    ) as session:

        tasks = []

        for person_id in range(1, 100):

            task = fetch_person(session, person_id)

            tasks.append(task)

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

        print(f"Loaded: {len(people)} characters")

        await save_people(people)


if __name__ == "__main__":
    asyncio.run(main())