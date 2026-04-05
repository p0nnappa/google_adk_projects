from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
# from google.adk.tools.mcp_tool import McpToolset, SseConnectionParams
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

import asyncio
from dotenv import load_dotenv
from pathlib import Path
from mcp.client.stdio import StdioServerParameters

load_dotenv()

APP_NAME = "basic_agent_no_web"
USER_ID = "user_12345"
SESSION_ID = "session_12345"

# step 1 : get the agent
async def get_agent():
    # Create an MCP toolset with the appropriate connection parameters
    toolset = McpToolset(
        # connection_params=SseConnectionParams(
        #     #url="http://127.0.0.1:8000/sse",
        #     url="https://livescoremcp.com/sse",
        # ), 
        connection_params=StreamableHTTPConnectionParams(
             # url="http://127.0.0.1:8000/mcp",
              url="https://hf.co/mcp",
        ),
    )

    root_agent = LlmAgent(
        name="first_agent",
        description="This is the first agent",
        instruction="You are a helpful assistant",
        model="gemini-2.5-flash",
        tools=[toolset]
    )
    return root_agent, toolset

#step 2 : run the agent
async def main(query):
   # create memory session 
    session_service = InMemorySessionService()
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    root_agent, toolset = await get_agent()
   # create runner agent
    runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=session_service)

    content = types.Content(role = "user", parts = [types.Part(text=query)])

    # run the agent
    events = runner.run_async(
        new_message=content,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    #print the events   
    async for event in events:
        if event.is_final_response():
            print("Final response: ", event.content.parts[0].text)

    await toolset.close()  # Ensure the mcp toolset connection is properly closed after use

if __name__ == "__main__":
    # query = "How is the weather in Mysore?"
    # query = "How many goals Messi has scored in his international career so far?" # https://livescoremcp.com/sse allows only football score
    # query = "Can you list all mcp servers available?"
    query = "Can you list all Hugging Face Spaces that are MCP enabled?"

    asyncio.run(main(query))