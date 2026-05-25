import asyncio
from typing import Any

import aiohttp


BASE_URL = "https://www.swapi.tech/api/people"

MAX_CONCURRENT_REQUESTS = 10

semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

planet_cache: dict[str, str | None] = {}


async def fetch_json(
    session: aiohttp.ClientSession,
    url: str,
    retries: int = 3,
) -> dict[str, Any] | None:

    for attempt in range(retries):

        try:

            async with semaphore:

                async with session.get(url) as response:

                    if response.status == 404:
                        return None

                    response.raise_for_status()

                    return await response.json()

        except (
            aiohttp.ClientError,
            asyncio.TimeoutError,
        ) as error:

            print(
                f"URL: {url} | "
                f"Error: {type(error).__name__}: {error}"
            )

            if attempt == retries - 1:
                return None

            await asyncio.sleep(1)


async def fetch_planet_name(
    session: aiohttp.ClientSession,
    planet_url: str | None,
) -> str | None:

    if not planet_url:
        return None

    if planet_url in planet_cache:
        return planet_cache[planet_url]

    data = await fetch_json(session, planet_url)

    if not data:
        return None

    planet_name = (
        data.get("result", {})
        .get("properties", {})
        .get("name")
    )

    planet_cache[planet_url] = planet_name

    return planet_name


async def fetch_person(
    session: aiohttp.ClientSession,
    person_id: int,
) -> dict[str, Any] | None:

    url = f"{BASE_URL}/{person_id}"

    data = await fetch_json(session, url)

    if not data:
        return None

    result = data.get("result")

    if not result:
        return None

    properties = result.get("properties")

    if not properties:
        return None

    homeworld_name = await fetch_planet_name(
        session,
        properties.get("homeworld"),
    )

    return {
        "id": person_id,
        "birth_year": properties.get("birth_year"),
        "eye_color": properties.get("eye_color"),
        "gender": properties.get("gender"),
        "hair_color": properties.get("hair_color"),
        "homeworld": homeworld_name,
        "mass": properties.get("mass"),
        "name": properties.get("name"),
        "skin_color": properties.get("skin_color"),
    }


async def fetch_people_page(
    session: aiohttp.ClientSession,
    page: int = 1,
    limit: int = 10,
) -> list[dict[str, Any]]:

    url = f"{BASE_URL}?page={page}&limit={limit}"

    data = await fetch_json(session, url)

    if not data:
        return []

    return data.get("results", [])


async def get_all_people_ids(
    session: aiohttp.ClientSession,
) -> list[int]:

    page = 1

    ids = set()

    while True:

        url = f"{BASE_URL}?page={page}&limit=10"

        data = await fetch_json(session, url)

        if not data:
            break

        people = data.get("results", [])

        if not people:
            break

        for person in people:

            uid = person.get("uid")

            if uid and uid.isdigit():
                ids.add(int(uid))

        next_page = data.get("next")

        if not next_page:
            break

        page += 1

    return list(ids)