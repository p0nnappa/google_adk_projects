from mcp.server.fastmcp import FastMCP
import requests

#create a FastMCP server instance
mcp_server = FastMCP("Weather Service", "Provides weather information for a given location.")

@mcp_server.tool("get_weather", "Fetches weather information for a given city.")
def get_weather(city:str) -> str:
    """Fetches weather information for a given city using wttr.in API."""
    try:
        endpoint_domain = "https://wttr.in"
        #response = requests.get(f"{endpoint_domain}/{city}?format=3") #gives only temperature
        response = requests.get(f"{endpoint_domain}/{city}") #gives only temperature

        if response.status_code == 200:
            return response.text
        else:
            return f"Could not fetch weather data for {city}. Please try again later."
    except Exception as e:
        return f"An error occurred while fetching weather data: {str(e)}"

if __name__ == "__main__":
    # mcp_server.run(transport="sse")
    mcp_server.run(transport="streamable-http")

