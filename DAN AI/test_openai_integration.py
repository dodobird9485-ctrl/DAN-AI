#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("[ERROR] GOOGLE_API_KEY not found in .env")
    exit(1)

print("[OK] Google API Key found")

try:
    from agent_advanced import AdvancedAgent
    print("[OK] Agent imported successfully")
    
    agent = AdvancedAgent()
    print("[OK] Agent instance created")
    
    print("[OK] Policy loaded: " + agent.policy['name'])
    print("[OK] Personality: " + agent.policy['personality'])
    print("[OK] Memory loaded: " + str(len(agent.memory)) + " items")
    
    print("\n--- Testing agent response ---")
    test_input = "What is Python?"
    print("Input: " + test_input)
    response = agent.respond(test_input)
    print("Response: " + response[:200] + "..." if len(response) > 200 else "Response: " + response)
    
    print("\n[SUCCESS] Google Gemini integration successful!")
    
except Exception as e:
    print("[ERROR] " + str(e))
    import traceback
    traceback.print_exc()
    exit(1)
