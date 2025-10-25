from mcp.server.fastmcp import FastMCP
import requests
import dotenv
import os
from DataBase import get_all_cities, get_attractions


mcp = FastMCP("database-mcp")

@mcp.tool()
def get_cities() -> dict:
    """Get all available cities for trip planning"""
    try:
        cities = get_all_cities()
    
        if not cities:
            return {
                "status": "error",
                "message": f"No cities found"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    return {
        "status": "success",
        "cities": cities,
        "count": len(cities)
    }
    


@mcp.tool()
def get_top_attractions(city: str) -> dict:
    """Get top 3 attractions for a city"""
    try:
        attractions = get_attractions(city)
    
        if not attractions:
            return {
                "status": "error",
                "message": f"No attractions found for {city}"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
    return {
        "status": "success",
        "city": city,
        "attractions": attractions,
        "count": len(attractions)
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")