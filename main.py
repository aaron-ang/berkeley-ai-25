import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from dotenv import load_dotenv

load_dotenv()


async def connect_to_server():
    """Connect to an MCP server"""
    async with streamablehttp_client("https://mcp.deepwiki.com/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # List available tools
            response = await session.list_tools()
            tools = response.tools
            print("\nConnected to server  with tools:", [tool.name for tool in tools])

            # Call a tool
            tool = tools[1]  # Select the first tool
            print(f"\nCalling tool: {tool}")
            response = await session.call_tool(
                tool.name, {"repoName": "microsoft/vscode"}
            )
            print(f"Tool response: {response}")


async def main():
    await connect_to_server()


if __name__ == "__main__":
    asyncio.run(main())
