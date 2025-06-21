import os
import asyncio
from dotenv import load_dotenv

from mcp_client import MCPClient


load_dotenv()

LETTA_API_KEY = os.getenv("LETTA_API_KEY")


async def main():
    async with MCPClient("https://mcp.deepwiki.com/mcp") as client:
        tools = await client.list_tools()
        print("\nConnected to server with tools:", tools)

        # Call a tool
        tool = tools[2]  # Select the first tool
        response = await client.call_tool(
            tool,
            {
                "repoName": "microsoft/vscode",
                "question": "How do I build the project locally? ",
            },
        )
        print(f"Tool response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
