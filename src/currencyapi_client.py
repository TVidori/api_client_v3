import asyncio
import aiohttp
import tenacity

API_BASE_URL = "https://api.currencyapi.com/v3"
API_KEY = "cur_live_85oFw09cvfo3TFJ7vIjVb8GAXw7qiBlRLjBciQHc"


class CurrencyApiClient:

    def __init__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
        )

    async def close(self) -> None:
        await self.session.close()

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(10),
        wait=tenacity.wait_fixed(3),
        reraise=True,
    )
    async def get_request(
            self,
            endpoint: str,
            to_json: bool = False,
    ) -> dict | aiohttp.ClientResponse:
        # await asyncio.sleep(6)  # Uncomment to safeguard against rate limit

        response = await self.session.get(
            url=f"{API_BASE_URL}/{endpoint}",
            headers={"apikey": API_KEY},
        )
        if to_json:
            return await response.json()
        else:
            return response

    async def print_latest_currency_exchange(self) -> None:
        response = await self.get_request(
            endpoint="latest",
            to_json=True
        )
        print(response)

    async def get_currency_historical_exchange(
            self,
            date: str,
            currency: str,
    ) -> float:
        response = await self.get_request(
            endpoint=f"historical?date={date}",
            to_json=True
        )
        return response["data"][currency]["value"]
