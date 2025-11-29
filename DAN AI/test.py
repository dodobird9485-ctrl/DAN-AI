from agent import Agent

agent = Agent("policy.json")
print("\n=== Testing Agent with All Tools ===")
print(f"Policy Name: {agent.policy['name']}\n")

test_queries = [
    "What is 5 + 3?",
    "Remember this: my favorite color is blue",
    "What if the condition is true then execute",
    "Classify this request",
    "Summarize this long text: The quick brown fox jumps over the lazy dog and continues running through the forest",
    "Fetch data from the website",
    "Query the database",
    "Make an API call",
    "Write this to file",
    "Translate this to Spanish",
    "Analyze sentiment",
    "Extract important data",
    "Generate a poem",
    'Parse this JSON {"name": "John", "age": 30}',
    "Calculate statistics for the dataset",
    "Validate the input",
    "Compare A vs B",
    "Execute this code",
    "Schedule a meeting tomorrow",
    "Who invented the light bulb?"
]

for query in test_queries:
    print(f"Query: {query}")
    response = agent.think(query)
    print(f"Response: {response}\n")

print("\n=== Audit Log ===")
print(f"Total audit entries: {len(agent.audit_log)}")
print(f"Memory stored: {agent.memory}")
print(f"Total requests: {agent.request_count}")

print("\n=== Enabled Tools ===")
print(f"Total tools enabled: {len(agent.policy['tools_enabled'])}")
print("Tools:", ", ".join(agent.policy['tools_enabled']))
