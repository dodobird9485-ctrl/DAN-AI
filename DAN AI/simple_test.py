print("Testing agent...")

try:
    from agent import Agent
    print("✓ Agent imported successfully")
    
    agent = Agent("policy.json")
    print("✓ Policy loaded successfully")
    print(f"✓ Policy name: {agent.policy['name']}")
    
    response = agent.think("Calculate 5 + 3")
    print(f"✓ Agent response: {response}")
    
    print("\n✅ Agent is working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\nNow testing Flask...")

try:
    import flask
    print("✓ Flask imported successfully")
    print("✓ Flask version: " + flask.__version__)
    
except ImportError as e:
    print(f"❌ Flask not installed: {e}")
    print("\nFix: Run this in command prompt:")
    print("pip install flask")
