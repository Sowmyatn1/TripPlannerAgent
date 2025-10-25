
"""
this the mcp server code i have built a custom mcp server here , which will give weather update
this way of builkding mcp server then The server can only be accessed locally by programs 
that start it or connect via stdio.

run hte server : uv run main.py
and client : uv run mcpclient.py
"""
from mcp.server.fastmcp import FastMCP
import requests
import dotenv
import os

dotenv.load_dotenv()

api_key = os.getenv("weatherAPIKey")

mcp = FastMCP("weather-mcp")

@mcp.tool()
def get_weather(city: str):
    """
    Get the current weather for a city using the WeatherAPI.com service.
    """
    if not api_key:
        return {"error": "API key not found. Please set 'weatherAPIKey' in your .env file."}

    # ✅ WeatherAPI.com endpoint
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    print(f"URL use here is : {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        weather = {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
        }

        print(f"🌤️ {weather['city']}, {weather['country']}: {weather['temperature']}°C, {weather['condition']}")
        return weather

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}




@mcp.resource("greeting://{name}")

def get_greeting(name: str):
    """
    Get a greeting for a person by name.
    """
    return f"Hello, {name}!"


if __name__ == "__main__":
     print("✅ MCP server is running and waiting for connections...")
     mcp.run(transport="stdio")
