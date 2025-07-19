from collections.abc import AsyncGenerator

from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client, StdioServerParameters


async def start_sse_session(url: str) -> AsyncGenerator[ClientSession]:
    async with sse_client(url) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        yield session

async def start_stdio_session(params: StdioServerParameters) -> AsyncGenerator[ClientSession]:
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        yield session


