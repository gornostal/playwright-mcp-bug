#!/usr/bin/env python
import re
import asyncio
import logging
import shutil

from app.playwright_ctl import PlaywrightCtl
from app.utils.mcp import start_stdio_session
from mcp.client.stdio import StdioServerParameters


logger = logging.getLogger(__name__)


async def main() -> None:
    params = StdioServerParameters(
        command="npx",
        args=[
            "@playwright/mcp",
            "--isolated",
            "--config",
            "mcp-configs/playwright-mcp.json",
        ],
    )

    async for playwright_mcp in start_stdio_session(params):
        playwright_ctl = PlaywrightCtl(playwright_mcp)

        # 1. Navigate to website
        snapshot = await playwright_ctl.call_tool(
            "browser_navigate", {"url": "https://ext.ulauncher.io"}
        )
        print("▶ Snapshot:", snapshot)

        # 2. Click on the "Log In" button
        match = re.search(r'button "Log In" \[ref=(\w+)\]', snapshot)
        assert match, "No button found in snapshot"
        ref = match.group(1)
        print("▶ Found Log In button ref:", ref)
        snapshot = await playwright_ctl.call_tool(
            "browser_click", {"ref": ref, "element": "button"}
        )
        print("▶ Button click result:", snapshot)

        # 3. Click Continue with GitHub   <-- this is where it crashes
        match = re.search(r"generic \[ref=(\w+)\] .* Continue with GitHub", snapshot)
        assert match, "No Continue with GitHub button found in snapshot"
        ref = match.group(1)
        print("▶ Found Continue with GitHub button ref:", ref)
        snapshot = await playwright_ctl.call_tool(
            "browser_click", {"ref": ref, "element": "button"}
        )
        print("▶ Continue with GitHub button click result:", snapshot)


if __name__ == "__main__":
    if not shutil.which("npx"):
        msg = "npx is not installed. Please install it with `npm install -g npx`."
        raise RuntimeError(msg)

    asyncio.run(main())
