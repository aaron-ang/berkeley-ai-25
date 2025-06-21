import time

from mcp import ClientSession, Tool
from mcp.client.streamable_http import streamablehttp_client


class MCPClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self._connection = None
        self._session = None
        self._read_stream = None
        self._write_stream = None

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._disconnect()

    async def _connect(self):
        """Connect to the MCP server and return a session."""
        if self._session is not None:
            return self._session

        self._connection = streamablehttp_client(self.server_url)
        self._read_stream, self._write_stream, _ = await self._connection.__aenter__()

        self._session = await ClientSession(
            self._read_stream, self._write_stream
        ).__aenter__()
        await self._session.initialize()
        return self._session

    async def _disconnect(self):
        """Disconnect from the MCP server."""
        if self._session:
            await self._session.__aexit__(None, None, None)
            self._session = None
        if self._connection:
            await self._connection.__aexit__(None, None, None)
            self._connection = None
        self._session = None
        self._read_stream = None
        self._write_stream = None

    async def list_tools(self):
        """List available tools on the MCP server."""
        if not self._session:
            raise RuntimeError(
                "Session is not initialized. Use `async with MCPClient` to connect."
            )

        response = await self._session.list_tools()
        return response.tools

    async def call_tool(self, tool: Tool, args=None):
        if not self._session:
            raise RuntimeError(
                "Session is not initialized. Use `async with MCPClient` to connect."
            )

        print(f"\nCalling tool: {tool.name}")
        start_time = time.time()
        response = await self._session.call_tool(tool.name, args)
        end_time = time.time()
        print(f"Tool call took {end_time - start_time:.2f} seconds")
        return response
