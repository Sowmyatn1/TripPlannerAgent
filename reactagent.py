"""LangGraph ReAct Agent with MCP - Using mcp.json"""

import os
import json
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

load_dotenv()


async def run_agent():
    """Run the ReAct agent with MCP tools"""
    
    print("🚀 Initializing MCP-enabled React Agent")
    print("=" * 70)
    
    # Load MCP config from mcp.json
    print("📂 Loading mcp.json config...")
    with open("mcp.json", "r", encoding="utf-8") as f:
        mcp_config = json.load(f)
    
    print(f"✅ Loaded config with {len(mcp_config['mcpServers'])} servers")
    for server_name in mcp_config["mcpServers"].keys():
        print(f"   - {server_name}")
    
    # Initialize MultiServerMCPClient with mcp.json config
    print("\n📡 Connecting to MCP servers...")
    client = MultiServerMCPClient(mcp_config["mcpServers"])
    
    # Get tools from all servers
    print("🔧 Loading tools from MCP servers...")
    try:
        tools = await asyncio.wait_for(client.get_tools(), timeout=30)
        print(f"✅ Loaded {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
    except asyncio.TimeoutError:
        print("❌ Timeout while loading tools. One or more MCP servers failed to start.")
        print("   Check that all servers in mcp.json can run independently:")
        for server_name in mcp_config["mcpServers"].keys():
            print(f"   - {server_name}")
        raise
    except Exception as e:
        print(f"❌ Error loading tools: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    # Initialize OpenAI model
    print("\n🤖 Initializing OpenAI LLM...")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("❌ OPENAI_API_KEY not set. Set it in .env or export it.")
    
    model = init_chat_model(
        model="openai:gpt-4o",
        api_key=openai_api_key
    )
    
    # Create React agent
    print("🔄 Creating React agent...")
    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt="You are a helpful trip planning assistant with access to attractions, accommodations, weather, and search tools."
    )
    
    print("\n" + "=" * 70)
    print("✅ Agent Ready!")
    print("=" * 70)
    
    # Interactive mode
    try:
        while True:
            user_input = input("\n📝 Enter your query (or 'quit' to exit):\nYou: ").strip()
            
            if user_input.lower() == "quit":
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\n🤖 Agent is thinking…")
            print("-" * 70)
            
            try:
                # Invoke agent with proper message format
                agent_response = await agent.ainvoke(
                    {"messages": [HumanMessage(content=user_input)]}
                )
                
                # Extract and print final response
                final_response = agent_response["messages"][-1].content
                print(f"\n✅ Agent Response:\n{final_response}")
            
            except Exception as e:
                print(f"❌ Agent Error: {e}")
                import traceback
                traceback.print_exc()
            
            print("-" * 70)
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_agent())