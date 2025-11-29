#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from agent_advanced import AdvancedAgent

load_dotenv()

try:
    agent = AdvancedAgent()
    print("[OK] Agent created\n")
    
    print("--- Testing web search ---\n")
    
    test_searches = [
        "Python tutorials",
        "JavaScript frameworks",
        "Learn web development"
    ]
    
    for query in test_searches:
        print(f"Query: {query}")
        response = agent.respond(f"search {query}")
        print(response)
        print("\n" + "="*60 + "\n")
    
except Exception as e:
    print(f"[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
