from agent_v2 import Agent

print("\n" + "="*60)
print("🤖 AI AGENT - Simple Version")
print("="*60 + "\n")

agent = Agent("policy.json")

print(f"Policy: {agent.policy['name']}")
print(f"Personality: {agent.policy['personality']}")
print("\nType 'exit' to quit\n")
print("-"*60 + "\n")

while True:
    user_input = input("You: ").strip()
    
    if not user_input:
        continue
    
    if user_input.lower() == "exit":
        print("\nGoodbye!\n")
        break
    
    response = agent.respond(user_input)
    print(f"Agent: {response}\n")
