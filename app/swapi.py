import asyncio
from typing import Any

import aiohttp


BASE_URL = "https://www.swapi.tech/api/people"

MAX_CONCURRENT_REQUESTS = 10

semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


async def fetch_json(
    session: aiohttp.ClientSession,
    url: str,
    retries: int = 2,
):

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

    return {
        "id": person_id,
        "birth_year": properties.get("birth_year"),
        "eye_color": properties.get("eye_color"),
        "gender": properties.get("gender"),
        "hair_color": properties.get("hair_color"),
        "homeworld": properties.get("homeworld"),
        "mass": properties.get("mass"),
        "name": properties.get("name"),
        "skin_color": properties.get("skin_color"),
    }