import asyncio
from duckduckgo_search import AsyncDDGS



async def get_results():
    async with AsyncDDGS() as ddgs:
        async for result in ddgs.text("metasploit", max_results=5):
            print(result['href'])

asyncio.run(get_results())