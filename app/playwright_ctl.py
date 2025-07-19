from typing import Any

from mcp import ClientSession
from mcp.types import TextContent


class PlaywrightCtl:
    def __init__(self, session: ClientSession) -> None:
        self.session = session

    async def get_tools(self, allowed_playwright_tools: list[str]) -> list[dict[str, Any]]:
        response = await self.session.list_tools()
        to_be_found = set(allowed_playwright_tools or [])
        found: list[dict[str, Any]] = []
        for t in response.tools:
            if t.name in to_be_found:
                found.append(
                    {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.inputSchema,
                    }
                )
                to_be_found.remove(t.name)
        if to_be_found:
            raise ValueError(f"Some tools were not found: {to_be_found}")

        return found

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        """
        Call a Playwright tool with the given name and arguments.
        """
        print(f"Tool {tool_name} called with arguments {arguments}")
        result = await self.session.call_tool(tool_name, arguments)
        assert not result.isError, str(result)
        assert result.content, str(result)
        assert len(result.content) > 0, str(result)
        assert isinstance(result.content[0], TextContent), str(result)

        return result.content[0].text
