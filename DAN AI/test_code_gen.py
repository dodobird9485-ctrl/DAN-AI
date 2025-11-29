#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from agent_advanced import AdvancedAgent

load_dotenv()

try:
    agent = AdvancedAgent()
    print("[OK] Agent created")
    
    print("\n--- Testing code generation ---")
    
    test_requests = [
        "create a simple python calculator",
        "make a python game launcher",
        "build a simple ESP WiFi scanner"
    ]
    
    for request in test_requests:
        print(f"\nRequest: {request}")
        response = agent.respond(request)
        print(f"Response: {response[:300]}...")
    
    print("\n[OK] Generated files:")
    for f in os.listdir('.'):
        if f.startswith('generated_'):
            print(f"  - {f}")
    
except Exception as e:
    print(f"[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
