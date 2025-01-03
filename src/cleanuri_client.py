import aiohttp
import aiohttp_proxy
import tenacity

API_BASE_URL = "https://cleanuri.com/api/v1"


class CleanuriClient:

    def __init__(
            self,
            proxy_url: str | None = None,
    ):
        timeout = aiohttp.ClientTimeout(total=30)
        if proxy_url is not None:
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                connector=aiohttp_proxy.ProxyConnector.from_url(proxy_url),
            )
        else:
            self.session = aiohttp.ClientSession(
                timeout=timeout,
            )

    async def close(self) -> None:
        await self.session.close()

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(10),
        wait=tenacity.wait_fixed(3),
        reraise=True,
    )
    async def post_request(
            self,
            endpoint: str,
            data: dict,
            to_json: bool = False,
    ) -> dict | aiohttp.ClientResponse:
        response = await self.session.post(
            url=f"{API_BASE_URL}/{endpoint}",
            data=data,
        )
        if to_json:
            return await response.json()
        else:
            return response

    async def post_shorten_url(
            self,
            url: str,
    ) -> str:
        response = await self.post_request(
            endpoint="shorten",
            data={"url": url},
            to_json=True,
        )
        return response["result_url"]
