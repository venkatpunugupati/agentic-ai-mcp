agentic-ai-mcp
Model Context Protocol (MCP) server and client in Python, built on the official MCP Python SDK (v2). The server exposes three tools, two resources, and one prompt over stdio, with a Streamable HTTP transport option. A minimal client and a VS Code configuration are included.
Contents
mcp_server.py — the MCP server
mcp_client.py — a stdio client
.vscode/mcp.json — VS Code MCP server configuration
Tools
Tool
Description
word_count(text)
Counts the words in the given text.
calculator(expression)
Evaluates an arithmetic expression.
get_current_time()
Returns the current local date and time.
Tools are model-controlled: the model decides when to call them and with what arguments. Each tool's description comes from its function docstring.
Resources
URI
Description
venkat://calculator-rules
Static rules for the calculator tool.
venkat://tool/{name}
Template resource returning the docstring for a named tool.
Resources are application-controlled, read-only context — the application decides when the model sees them.
Prompts
Prompt
Description
fox_times_three(multiplier="3")
A reusable prompt that counts the words in the fox sentence and multiplies by the given multiplier.
Prompts are application-controlled templates the user (or client) invokes; the model fills in the rest.
Setup
Requires Python 3.10+ and the MCP Python SDK v2:
python -m venv .venv
source .venv/bin/activate
pip install mcp
Run the server
python mcp_server.py
The server speaks stdio by default — no print() output on stdout, so the protocol stream stays clean. For Streamable HTTP:
mcp.run(transport="streamable-http", port=8000)
then connect to http://127.0.0.1:8000/mcp.
Inspect it
With the MCP Inspector:
mcp dev mcp_server.py
Open the Inspector at http://127.0.0.1:6274, connect, and verify the three tools, the resources, and the prompt. Expected results: word_count on the fox sentence returns 9, calculator("240*0.15") returns 36.0.
Run the client
python mcp_client.py
The client connects over stdio, lists the server's tools, and calls them — word_count → 9, calculator("240*0.15") → 36.0 — plus a resource read and a prompt render.
VS Code
.vscode/mcp.json registers the server with VS Code under the name venkat-tools. Update the command (Python interpreter) and the server path in args to match your machine.
Notes
The server keeps no state between runs; each client connection gets its own server process over stdio.
Over HTTP, one server process serves multiple clients, with sessions tracked by ID.
