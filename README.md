# mcp-integration
Proof of Concept showcasing Mode Context Protocol (MCP) integration with Claude AI to analyze personal data fetched via Server-Sent Events (SSE).

# mcp-integration
Proof of Concept showcasing Mode Context Protocol (MCP) integration with Claude AI to analyze personal data fetched via Server-Sent Events (SSE).

**What is MCP**

MCP is an open protocol that standardizes how applications provide context to LLMs. Think of MCP like a USB-C port for AI applications. Just as USB-C provides a standardized way to connect your devices to various peripherals and accessories, MCP provides a standardized way to connect AI models to different data sources and tools.
[More Info
]([https://](https://modelcontextprotocol.io/introduction))

**Setup MCP**

[Follow this](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#installation)

**Usage**
```python

python server.py

INFO:     Started server process [4992]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:51226 - "POST /sse HTTP/1.1" 405 Method Not Allowed
INFO:     127.0.0.1:51226 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:51227 - "POST /messages/?session_id=9a1abb94b13f457f8c90de15ee80bd2e HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:51227 - "POST /messages/?session_id=9a1abb94b13f457f8c90de15ee80bd2e HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:51228 - "POST /messages/?session_id=9a1abb94b13f457f8c90de15ee80bd2e HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:51229 - "POST /messages/?session_id=9a1abb94b13f457f8c90de15ee80bd2e HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:51230 - "POST /messages/?session_id=9a1abb94b13f457f8c90de15ee80bd2e HTTP/1.1" 202 Accepted
[05/24/25 12:47:56] INFO     Processing request of type        server.py:551
                             ListToolsRequest
                    INFO     Processing request of type        server.py:551
                             ListResourcesRequest
                    INFO     Processing request of type        server.py:551
                             ListToolsRequest

```

**Configuring Claude**

[Download claude](https://claude.ai/download)
[Configure MCP server](https://appwrite.io/docs/tooling/mcp/claude#step-1)


**MCP Config**

````json
{
  "mcpServers": {
    "diet": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://127.0.0.1:8000/sse"
      ]
    }
  }
}
````


