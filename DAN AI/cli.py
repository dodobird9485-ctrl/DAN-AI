#!/usr/bin/env python3
from agent import Agent
import sys

def main():
    print("\n" + "="*60)
    print("🤖 AI AGENT - Command Line Interface")
    print("="*60)
    
    try:
        agent = Agent("policy.json")
        print(f"\n✓ Agent loaded: {agent.policy['name']}")
        print(f"✓ Personality: {agent.policy['personality']}")
        print(f"✓ Tools enabled: {len(agent.policy['tools_enabled'])}")
    except Exception as e:
        print(f"\n❌ Error loading agent: {e}")
        return
    
    print("\nCommands:")
    print("  Type 'exit' to quit")
    print("  Type 'policy' to see current policy")
    print("  Type 'reload' to reload policy")
    print("  Type 'tools' to see all tools")
    print("  Type 'memory' to see stored memories")
    print("\nExamples:")
    print("  Calculate 5 + 3")
    print("  Remember my favorite color is blue")
    print("  Translate hello to Spanish")
    print("  Generate a funny poem")
    print("\n" + "-"*60 + "\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print("\nGoodbye! 👋\n")
                break
            
            elif user_input.lower() == "policy":
                import json
                print("\n" + json.dumps(agent.policy, indent=2) + "\n")
                continue
            
            elif user_input.lower() == "reload":
                agent.reload_policy("policy.json")
                print(f"\n✓ Policy reloaded: {agent.policy['name']}\n")
                continue
            
            elif user_input.lower() == "tools":
                print("\nAvailable tools:")
                for i, tool in enumerate(agent.policy['tools_enabled'], 1):
                    print(f"  {i}. {tool}")
                print()
                continue
            
            elif user_input.lower() == "memory":
                if agent.memory:
                    print("\nStored memories:")
                    for key, value in agent.memory.items():
                        print(f"  • {key}: {value}")
                else:
                    print("\nNo stored memories yet")
                print()
                continue
            
            print(f"\nAgent: {agent.think(user_input)}\n")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()
