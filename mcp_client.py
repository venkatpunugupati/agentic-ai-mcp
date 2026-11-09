import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

SERVER = "/Users/venkatpunugupati/Desktop/AI_Python/mcp/mcp_server.py"
PYTHON = "/Users/venkatpunugupati/Desktop/AI_Python/langgraph/.venv/bin/python"
FOX = "the quick brown fox jumps over the lazy dog"


async def main():
    server_params = StdioServerParameters(command=PYTHON, args=[SERVER])
    #async with stdio_client(server_params) as (read, write): # stdio
        #async with ClientSession(read, write) as session: # stdio
    async with streamable_http_client("http://127.0.0.1:8000/mcp") as (read, write):
        async with ClientSession(read, write) as session:   
            await session.initialize()
            #print("connected, waiting...")
            #await asyncio.sleep(30) # For testing multiple clients , wait for 30 seconds before sending requests

            tools = await session.list_tools()
            print("tools:", [t.name for t in tools.tools])

            wc = await session.call_tool("word_count", arguments={"text": FOX})
            print("word_count:", wc.content[0].text)

            calc = await session.call_tool("calculator", arguments={"expression": "240*0.15"})
            print("calculator:", calc.content[0].text)

            resources = await session.list_resources()
            print("resources:", [str(r.uri) for r in resources.resources])

            doc = await session.read_resource("venkat://tool/word_count")
            print("word_count doc:", doc.contents[0].text)

            prompts = await session.list_prompts()
            print("prompts:", [p.name for p in prompts.prompts])

            prompt = await session.get_prompt("fox_times_three", arguments={"multiplier": "5"})
            for m in prompt.messages:
                print(f"prompt message [{m.role}]: {m.content.text}")


if __name__ == "__main__":
    asyncio.run(main())
