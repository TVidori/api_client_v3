import asyncio

from src.currencyapi_client import CurrencyApiClient
from src.cleanuri_client import CleanuriClient


async def collect_all_data():
    urls_to_collect = [
        "https://ok.ru",
        "https://ebay.com",
        "https://fb.me",
        "https://nhk.or.jp",
        "https://timeweb.ru",
        "https://www.canalblog.com",
        "https://lemonde.fr",
        "https://office.com",
        "https://ucla.edu",
        "https://shutterstock.com",
        "https://terra.com.br",
        "https://aljazeera.com",
        "https://dropcatch.com",
        "https://cbsnews.com",
        "https://bit.ly"
    ]
    cleanuri_proxy_urls = [
        None,
        None,
    ]
    co_routines = [call_currencyapi_client_endpoints()] + [
        collect_shorten_urls_from_cleanuri(
            urls_to_collect=urls_to_collect,
            proxy_url=proxy_url
        )
        for proxy_url in cleanuri_proxy_urls
    ]
    await asyncio.gather(*co_routines)


async def call_currencyapi_client_endpoints() -> None:
    print("Start currencyapi collection")
    client = CurrencyApiClient()
    await client.print_latest_currency_exchange()
    euros_value = await client.get_currency_historical_exchange(
        date="2022-01-01",
        currency="EUR"
    )
    print(euros_value)

    await client.close()
    print("End of currencyapi collection")


async def collect_shorten_urls_from_cleanuri(
        urls_to_collect: list[str],
        proxy_url: str | None = None,
) -> None:
    print("Start cleanuri collection")
    cleanuri_client = CleanuriClient(
        proxy_url=proxy_url
    )

    shorten_urls = []
    while len(urls_to_collect) > 0:
        url = urls_to_collect.pop()
        shorten_urls.append(await cleanuri_client.post_shorten_url(
            url=url,
        ))

    await cleanuri_client.close()
    print(shorten_urls)
    print("End of cleanuri collection")


if __name__ == "__main__":
    asyncio.run(collect_all_data())
