import json
import os
from datetime import datetime

class Agent:
    def __init__(self, policy_file="policy.json"):
        self.policy_file = policy_file
        self.load_policy()
        self.memory = {}
        self.logs = []
    
    def load_policy(self):
        with open(self.policy_file, 'r') as f:
            self.policy = json.load(f)
    
    def respond(self, user_input):
        response = f"[{self.policy['personality']}] "
        user_lower = user_input.lower()
        
        if '+' in user_input or '-' in user_input or '*' in user_input or '/' in user_input:
            try:
                result = eval(user_input)
                response += f"Result: {result}"
            except:
                response += "Could not calculate"
        
        elif "remember" in user_lower or "store" in user_lower:
            key = "memory_" + str(len(self.memory))
            self.memory[key] = user_input
            response += f"Stored: {user_input}"
        
        elif "translate" in user_lower:
            response += f"Translating: {user_input}"
        
        elif "generate" in user_lower or "create" in user_lower or "write" in user_lower:
            response += f"Creating: {user_input}"
        
        elif "?" in user_input:
            response += f"Searching for: {user_input}"
        
        else:
            response += f"You said: {user_input}"
        
        self.logs.append({"input": user_input, "output": response})
        return response
