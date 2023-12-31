import aiohttp, constants


async def get_wyr(rating: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{constants.WOULD_YOU_RATHER_ROUTE}?rating={rating}",
        ) as response:
            body = await response.json()

            if response.status != 200:
                raise Exception(f"{response.status}: {body}")

            return body["question"]
