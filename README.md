# 🌍 Trip Planner - MCP Agentic System
A fully functional AI-powered trip planning agent built with LangGraph, LangChain MCP Adapters, and OpenAI's GPT-4o. The system uses 4 independent MCP servers to provide attractions, search results, accommodation options, and weather information.
🎯 Features
```
✅ ReAct Agent - Reason and Act paradigm for intelligent tool selection
✅ 4 MCP Servers - Modular, independently running services
✅ Natural Language Interface - Conversational trip planning
✅ Real-time Tool Integration - Automatically discovers and uses available tools
✅ Timeout Handling - Graceful error management
✅ OpenAI GPT-4o - Advanced language model for reasoning
```
```

 ┌─────────────────────────────────────────────┐
 │              ReAct Agent (reactagent.py)    │
 │         LangGraph + OpenAI GPT-4o           │
 └──────────────────┬──────────────────────────┘
                    │
     ┌──────────────┴───────────────┐
     │           │           │      │
     ▼           ▼           ▼      ▼
 ┌─────────┐ ┌────────┐ ┌────────┐ ┌────────┐
 │Database │ │ Search │ │ Airbnb │ │Weather │
 │   MCP   │ │   MCP  │ │   MCP  │ │   MCP  │
 └─────────┘ └────────┘ └────────┘ └────────┘
     │           │           │          │
     ▼           ▼           ▼          ▼
  SQLite   DuckDuckGo   Mock Data   Mock Data


```


```

📁 Project Structure
TripPlannerMCP/
├── reactagent.py                    # Main ReAct Agent
├── mcp.json                         # MCP Configuration
├── requirements.txt                 # Python Dependencies
├── .env                            # Environment Variables
│
├── mcp_servers/
│   ├── __init__.py
│   ├── database_mcp.py             # Cities & Attractions
│   ├── websearch_mcp.py               # DuckDuckGo Search
│   ├── airbnb_mcp.py               # Accommodations
│   └── weather_mcp.py              # Weather Data
│
├── database/
│   ├── __init__.py
│   └── db.py                       # SQLite Database
│
└── README.md                        # This File


```

# 🚀 Quick Start

## Prerequisites

- Python 3.10+
- OpenAI API Key
- Terminal access (need 5 terminals)

## Installation 

1. Clone/Setup Project
     mkdir TripPlannerMCP
     cd TripPlannerMCP

3. Create Virtual Environment
      python -m venv venv
      source .venv/bin/activate

4. Install Dependencies
      pip install -r requirements.txt

5. Set Environment Variables
      Create .env file:


6. Start MCP Servers (Open 4 Terminals)
   
- **Terminal 1 - Database MCP:**
  uv run database_mcp.py
- **Terminal 2 - Search MCP:**
  uv run websearch_mcp.py
- **Terminal 3 - Airbnb MCP:**
  uv run airbnb_mcp.py
- **Terminal 4 - Weather MCP:**
  uv run weather_mcp.py

Wait for each to show: MCP server listening on stdio


8. Run Agent (New Terminal)
bashpython reactagent.py


# Expected output:

🚀 Initializing MCP-React Agent
======================================================================
- 📂 Loading mcp.json config...
- ✅ Loaded config with 4 servers
- 📡 Connecting to MCP servers...
- 🔧 Loading tools from MCP servers...
- ✅ Loaded 7 tools:
   - get_cities
   - get_top_attractions
   - search_attraction
   - get_visitor_tips
   - find_rentals
   - get_current_weather

🤖 Initializing OpenAI LLM...
🔄 Creating React agent...

 ## Agent Ready!


📝 Enter your query (or 'quit' to exit):
You:

💬 Usage Examples
Example 1: Simple Query
You: What attractions are in London?

Agent Response:
London offers several popular attractions:
1. Big Ben - Historic clock tower (Rating: 4.7/5)
2. Tower of London - Historic fortress (Rating: 4.6/5)
3. Buckingham Palace - Royal residence (Rating: 4.5/5)
Example 2: Budget Trip Planning
You: Plan a trip to Paris under $100/night

Agent Response:
I found great options for a Paris trip within your budget!

Top Attractions:
1. Eiffel Tower - Iron tower landmark (Rating: 4.8/5)
2. Louvre Museum - Art museum (Rating: 4.7/5)
3. Notre-Dame - Cathedral (Rating: 4.6/5)

Accommodations Under $100/night:
1. Marais District Loft - $65/night (Rating: 4.7/5)
2. Latin Quarter 3BR - $110/night (Rating: 4.5/5)

Current Weather: 14°C, Partly Cloudy
Example 3: Multi-step Query
You: Compare London and Paris for a romantic weekend

Agent Response:
[Compares attractions, weather, and accommodations for both cities]
Example 4: Weather-based Recommendations
You: Tell me about New York attractions and weather

Agent Response:
[Provides attractions and weather-appropriate recommendations]


==================================================================================================
# 🔧 Configuration
   
## mcp.json
```
Simple configuration file that registers all MCP servers:
json{
  "mcpServers": {
    "database-mcp": {
      "command": "python",
      "args": ["database_mcp.py"]
    },
    "search-mcp": {
      "command": "python",
      "args": ["websearch_mcp.py"]
    },
    "airbnb-mcp": {
      "command": "python",
      "args": ["airbnb_mcp.py"]
    },
    "weather-mcp": {
      "command": "python",
      "args": ["weather_mcp.py"]
    }
  }
}
```
## Environment Variables (.env)
  OPENAI_API_KEY=sk-your-key-here

# 📊 MCP Servers Overview

## Database MCP (database_mcp.py)

Purpose: Local SQLite database for cities and attractions
Tools:

get_cities() - Lists all available cities
get_top_attractions(city) - Returns top 3 attractions



## Search MCP (websearch_mcp.py)

Purpose: Search for detailed attraction information
Tools:

search_attraction(name, city) - Get detailed info using DuckDuckGo
get_visitor_tips(attraction) - Get visitor tips and practical info



## Airbnb MCP (airbnb_mcp.py)

Purpose: Find accommodation options
Tools:

find_rentals(city, budget) - Find rentals with optional budget filter



## Weather MCP (weather_mcp.py)

Purpose: Get current weather conditions
Tools:

get_current_weather(city) - Get current temperature, condition, and advice


```

🔄 Data Flow
User Input
    ↓
ReAct Agent (reactagent.py)
    ↓
MultiServerMCPClient
    ↓
mcp.json Configuration
    ↓
4 MCP Servers (parallel execution)
    ├─ database_mcp.py
    ├─ websearch_mcp.py
    ├─ airbnb_mcp.py
    └─ weather_mcp.py
    ↓
Agent Processes Results
    ↓
Synthesized Response
    ↓
User Output
```
