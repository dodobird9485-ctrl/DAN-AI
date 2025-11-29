from agent import Agent
import json
import sys

def main():
    agent = Agent("policy.json")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "interactive":
            agent.run_interactive()
        elif sys.argv[1] == "test":
            test_agent(agent)
        elif sys.argv[1] == "policy":
            print(json.dumps(agent.get_policy(), indent=2))
    else:
        print("Usage:")
        print("  python main.py interactive  - Run in interactive mode")
        print("  python main.py test         - Run test queries")
        print("  python main.py policy       - View current policy")

def test_agent(agent):
    test_queries = [
        "What is 5 + 3?",
        "Who invented the light bulb?",
        "Can you help me?"
    ]
    
    print(f"Testing with policy: {agent.policy['name']}\n")
    for query in test_queries:
        print(f"Query: {query}")
        response = agent.think(query)
        print(f"Response: {response}\n")

if __name__ == "__main__":
    main()
