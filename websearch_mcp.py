"""Search MCP Server using DuckDuckGo API — FASTMCP version"""

from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS

app = FastMCP(name="search-mcp")

def duckduckgo_search(query: str, max_results: int = 3) -> dict:
    """Helper function to search DuckDuckGo and format results"""
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=max_results)
        
        if not results:
            return {"source": "DuckDuckGo", "content": "No results found", "error": False}

        first = results[0]
        content = first.get("body", "")
        if len(content) > 300:
            content = content[:300] + "..."
        
        return {
            "source": "DuckDuckGo",
            "title": first.get("title", ""),
            "url": first.get("href", ""),
            "content": content
        }

    except Exception as e:
        return {
            "source": "DuckDuckGo",
            "error": True,
            "message": str(e)
        }


@app.tool()
def search_attraction(name: str, city: str) -> dict:
    """Search for detailed information about a tourist attraction"""
    query = f"{name} {city} tourist attraction information"
    result = duckduckgo_search(query)
    return {
        "status": "success",
        "attraction": name,
        "city": city,
        "information": result
    }


@app.tool()
def get_visitor_tips(attraction: str) -> dict:
    """Get visitor tips, opening hours, and entry fees for an attraction"""
    query = f"{attraction} visitor tips opening hours entry fee admission"
    result = duckduckgo_search(query)
    return {
        "status": "success",
        "attraction": attraction,
        "information": result
    }


if __name__ == "__main__":
    app.run(transport="stdio")
        