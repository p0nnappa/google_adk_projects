from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name = "first_agent",
    description = "This is the first agent",
    instruction = "You are a helpful assistant",
    model = "gemini-2.5-flash",
    
)