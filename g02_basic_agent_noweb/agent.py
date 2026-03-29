from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "basic_agent_no_web"
USER_ID = "user_12345"
SESSION_ID = "session_12345"

# step 1 : get the agent
async def get_agent():
    root_agent = LlmAgent(
        name = "first_agent",
        description = "This is the first agent",
        instruction = "You are a helpful assistant",
        model = "gemini-2.5-flash",
    )
    return root_agent

#step 2 : run the agent
async def main(query):
   # create memory session 
    session_service = InMemorySessionService()
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    root_agent = await get_agent()
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


if __name__ == "__main__":
    query = "What is the capital of Kodagu?"
    asyncio.run(main(query))