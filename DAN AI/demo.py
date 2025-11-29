from agent import Agent
import json

def demo_basic():
    print("\n" + "="*50)
    print("DEMO 1: Basic Agent")
    print("="*50)
    agent = Agent("policy.json")
    queries = [
        "Calculate 10 + 5",
        "Remember my birthday as December 25",
        "What is sentiment analysis?"
    ]
    for query in queries:
        print(f"\nQuery: {query}")
        print(f"Response: {agent.think(query)}")

def demo_policies():
    print("\n" + "="*50)
    print("DEMO 2: Switching Policies")
    print("="*50)
    
    agent = Agent("policy.json")
    print(f"\nCurrent Policy: {agent.policy['name']}")
    print(f"Tools: {len(agent.policy['tools_enabled'])} enabled")
    
    agent.update_policy({
        "name": "Quick Policy",
        "personality": "fast and direct",
        "tools_enabled": ["calculate", "search"]
    })
    
    print(f"\nUpdated Policy: {agent.policy['name']}")
    print(f"Tools: {len(agent.policy['tools_enabled'])} enabled")
    print(f"Response: {agent.think('What is 2 * 3?')}")

def demo_memory():
    print("\n" + "="*50)
    print("DEMO 3: Memory System")
    print("="*50)
    
    agent = Agent("policy.json")
    
    print("\nStoring memories...")
    print(agent.think("Remember my name is Alex"))
    print(agent.think("Store my email as alex@example.com"))
    
    print("\nRecall memories...")
    print(f"Stored memories: {json.dumps(agent.memory, indent=2)}")

def demo_audit():
    print("\n" + "="*50)
    print("DEMO 4: Audit Logging")
    print("="*50)
    
    agent = Agent("policy.json")
    
    print("\nExecuting actions...")
    agent.think("Validate the input")
    agent.think("Schedule meeting tomorrow")
    agent.think("Check rate limit")
    
    print(f"\nAudit Log ({len(agent.audit_log)} entries):")
    for entry in agent.audit_log:
        print(f"  - {entry['timestamp']}: {entry['action']}")

def demo_tools_showcase():
    print("\n" + "="*50)
    print("DEMO 5: All Tools Showcase")
    print("="*50)
    
    agent = Agent("policy.json")
    
    tools_demo = {
        "calculate": "What is 10 + 5 * 2?",
        "memory": "Remember this important fact",
        "logic": "If condition is true then proceed",
        "classify": "Classify this request type",
        "summarize": "Summarize this very long document with many words",
        "sentiment": "Analyze sentiment of this text",
        "translate": "Translate to Spanish",
        "extract": "Extract the key information",
        "generate": "Generate creative content",
        "statistics": "Calculate average statistics",
        "validate": "Validate this data",
        "compare": "Compare option A vs option B"
    }
    
    for tool, query in list(tools_demo.items())[:6]:
        print(f"\nTool: {tool}")
        print(f"Query: {query}")
        print(f"Result: {agent.think(query)}")

if __name__ == "__main__":
    print("\n🤖 AI AGENT DEMO - All Tools and Features")
    
    demo_basic()
    demo_policies()
    demo_memory()
    demo_audit()
    demo_tools_showcase()
    
    print("\n" + "="*50)
    print("Demo completed!")
    print("="*50)
