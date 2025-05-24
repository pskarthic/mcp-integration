from typing import Any
import csv
import io
import httpx
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
import uvicorn

# Initialize FastMCP server for Weather tools (SSE)
mcp = FastMCP("weather")

@mcp.tool()
async def get_echo(message) -> str:      
    return "\n---\n" + message

@mcp.tool()
async def get_diet_data() -> str:
    """Get diet data from a CSV file."""
    return convert_data_to_csv_string(read_single_csv_file("Diet_Chart_September_U.csv"))

def read_single_csv_file(file_path):
    """
    Reads a single CSV file and returns its content as a list of lists.
    The first sub-list will be the header, and subsequent sub-lists are data rows.
    """
    data = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def convert_data_to_csv_string(data):
    """
    Converts a list of lists (CSV data) into a single CSV formatted string.

    Args:
        data (list of lists): The CSV data, where each inner list is a row.

    Returns:
        str: A single string formatted as a CSV. Returns an empty string if data is None.
    """
    if data is None:
        return "" # Handle the case where read_single_csv_file returned None

    output = io.StringIO()
    # Use '\n' for lineterminator for cross-platform consistency
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(data)
    csv_string = output.getvalue()
    return csv_string

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can server the provied mcp server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )


if __name__ == "__main__":
    mcp_server = mcp._mcp_server



    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(mcp_server, debug=True)

    uvicorn.run(starlette_app, host='0.0.0.0', port=8000)