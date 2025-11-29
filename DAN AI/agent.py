import json
import os
from typing import Any, Dict, List
from datetime import datetime

class Agent:
    def __init__(self, policy_file: str = "policy.json"):
        self.policy = self._load_policy(policy_file)
        self.step_count = 0
        self.memory = {}
        self.audit_log = []
        self.request_count = 0
        
    def _load_policy(self, policy_file: str) -> Dict[str, Any]:
        if not os.path.exists(policy_file):
            raise FileNotFoundError(f"Policy file '{policy_file}' not found")
        with open(policy_file, 'r') as f:
            return json.load(f)
    
    def reload_policy(self, policy_file: str = "policy.json"):
        self.policy = self._load_policy(policy_file)
        self.step_count = 0
        if self.policy.get("verbose"):
            print(f"[Agent] Policy reloaded: {self.policy['name']}")
    
    def get_policy(self) -> Dict[str, Any]:
        return self.policy
    
    def update_policy(self, updates: Dict[str, Any]):
        self.policy.update(updates)
        if self.policy.get("verbose"):
            print(f"[Agent] Policy updated with: {list(updates.keys())}")
    
    def think(self, input_text: str) -> str:
        self.step_count = 0
        if self.policy.get("verbose"):
            print(f"\n[Agent] Personality: {self.policy.get('personality', 'N/A')}")
            print(f"[Agent] Goals: {', '.join(self.policy.get('goals', []))}")
            print(f"[Agent] Constraints: {', '.join(self.policy.get('constraints', []))}")
        
        response = self._process_input(input_text)
        return response
    
    def _process_input(self, input_text: str) -> str:
        max_steps = self.policy.get("max_steps", 5)
        enabled_tools = self.policy.get("tools_enabled", [])
        
        response = f"[{self.policy.get('personality')}] "
        
        for step in range(max_steps):
            self.step_count += 1
            
            if self.policy.get("verbose"):
                print(f"[Step {self.step_count}/{max_steps}]")
            
            tool_response = self._select_and_use_tool(input_text, enabled_tools)
            if tool_response:
                response += tool_response
                break
        
        return response
    
    def _select_and_use_tool(self, input_text: str, tools: List[str]) -> str:
        text_lower = input_text.lower()
        
        if "calculate" in tools and any(op in input_text for op in ["+", "-", "*", "/"]):
            return self._tool_calculate(input_text)
        elif "memory" in tools and any(word in text_lower for word in ["remember", "recall", "store", "save"]):
            return self._tool_memory(input_text)
        elif "logic" in tools and any(word in text_lower for word in ["if", "then", "condition", "logic"]):
            return self._tool_logic(input_text)
        elif "classify" in tools and any(word in text_lower for word in ["classify", "category", "type", "what kind"]):
            return self._tool_classify(input_text)
        elif "summarize" in tools and any(word in text_lower for word in ["summarize", "summary", "brief", "short"]):
            return self._tool_summarize(input_text)
        elif "fetch_url" in tools and any(word in text_lower for word in ["fetch", "url", "website", "download"]):
            return self._tool_fetch_url(input_text)
        elif "database" in tools and any(word in text_lower for word in ["database", "query", "store", "record"]):
            return self._tool_database(input_text)
        elif "api_call" in tools and any(word in text_lower for word in ["api", "request", "call"]):
            return self._tool_api_call(input_text)
        elif "file_io" in tools and any(word in text_lower for word in ["file", "read", "write", "save"]):
            return self._tool_file_io(input_text)
        elif "translate" in tools and any(word in text_lower for word in ["translate", "language", "spanish", "french"]):
            return self._tool_translate(input_text)
        elif "sentiment" in tools and any(word in text_lower for word in ["sentiment", "feeling", "emotion", "mood"]):
            return self._tool_sentiment(input_text)
        elif "extract" in tools and any(word in text_lower for word in ["extract", "pull", "find", "get data"]):
            return self._tool_extract(input_text)
        elif "generate" in tools and any(word in text_lower for word in ["generate", "create", "write", "compose"]):
            return self._tool_generate(input_text)
        elif "parse_json" in tools and "{" in input_text:
            return self._tool_parse_json(input_text)
        elif "statistics" in tools and any(word in text_lower for word in ["statistics", "average", "mean", "count", "total"]):
            return self._tool_statistics(input_text)
        elif "validate" in tools and any(word in text_lower for word in ["validate", "check", "verify"]):
            return self._tool_validate(input_text)
        elif "compare" in tools and any(word in text_lower for word in ["compare", "difference", "vs", "versus"]):
            return self._tool_compare(input_text)
        elif "execute_code" in tools and any(word in text_lower for word in ["execute", "run", "code", "script"]):
            return self._tool_execute_code(input_text)
        elif "schedule" in tools and any(word in text_lower for word in ["schedule", "plan", "later", "remind"]):
            return self._tool_schedule(input_text)
        elif "audit" in tools:
            return self._tool_audit(input_text)
        elif "rate_limit" in tools:
            return self._tool_rate_limit(input_text)
        elif "search" in tools and any(word in text_lower for word in ["what", "who", "where", "when", "search", "?"]):
            return self._tool_search(input_text)
        elif "reason" in tools:
            return self._tool_reason(input_text)
        
        return f"[{self.policy.get('personality')}] Got your message: {input_text}"
    
    def _tool_calculate(self, text: str) -> str:
        try:
            result = eval(text.replace("calculate ", "").replace("?", ""))
            return f"Calculation result: {result}"
        except:
            return "Could not perform calculation."
    
    def _tool_memory(self, text: str) -> str:
        if "remember" in text.lower() or "store" in text.lower():
            key = text.split("as")[-1].strip() if "as" in text else "memory"
            self.memory[key] = text
            return f"Stored in memory: {key}"
        else:
            return f"Memory contents: {json.dumps(self.memory, indent=2)}"
    
    def _tool_logic(self, text: str) -> str:
        return f"Evaluating logic: {text}"
    
    def _tool_classify(self, text: str) -> str:
        categories = ["urgent", "normal", "low-priority", "informational"]
        return f"Classified as: normal category"
    
    def _tool_summarize(self, text: str) -> str:
        words = text.split()
        summary = " ".join(words[:15]) + "..." if len(words) > 15 else text
        return f"Summary: {summary}"
    
    def _tool_fetch_url(self, text: str) -> str:
        return f"Fetching data from URL mentioned in: {text}"
    
    def _tool_database(self, text: str) -> str:
        return f"Database query executed for: {text}"
    
    def _tool_api_call(self, text: str) -> str:
        return f"API call made with parameters: {text}"
    
    def _tool_file_io(self, text: str) -> str:
        if "write" in text.lower() or "save" in text.lower():
            return f"File write operation: {text}"
        else:
            return f"File read operation: {text}"
    
    def _tool_translate(self, text: str) -> str:
        lang = "Spanish" if "spanish" in text.lower() else "French" if "french" in text.lower() else "Unknown"
        return f"Translating to {lang}: {text}"
    
    def _tool_sentiment(self, text: str) -> str:
        return f"Sentiment analysis: Neutral tone detected in '{text}'"
    
    def _tool_extract(self, text: str) -> str:
        return f"Extracted data from: {text}"
    
    def _tool_generate(self, text: str) -> str:
        return f"Generated content based on: {text}"
    
    def _tool_parse_json(self, text: str) -> str:
        try:
            data = json.loads(text[text.find("{"):text.rfind("}")+1])
            return f"Parsed JSON successfully: {json.dumps(data)}"
        except:
            return "Could not parse JSON"
    
    def _tool_statistics(self, text: str) -> str:
        return f"Computing statistics for: {text}"
    
    def _tool_validate(self, text: str) -> str:
        return f"Validation: All checks passed for '{text}'"
    
    def _tool_compare(self, text: str) -> str:
        return f"Comparison analysis: {text}"
    
    def _tool_execute_code(self, text: str) -> str:
        return f"Code execution prepared for: {text}"
    
    def _tool_schedule(self, text: str) -> str:
        return f"Scheduled task: {text} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    def _tool_audit(self, text: str) -> str:
        self.audit_log.append({"timestamp": datetime.now().isoformat(), "action": text})
        return f"Audit logged: {text} (Total logs: {len(self.audit_log)})"
    
    def _tool_rate_limit(self, text: str) -> str:
        self.request_count += 1
        max_requests = self.policy.get("max_requests", 100)
        return f"Request {self.request_count}/{max_requests}"
    
    def _tool_search(self, text: str) -> str:
        return f"Searching for information about: {text}"
    
    def _tool_reason(self, text: str) -> str:
        constraints = self.policy.get("constraints", [])
        return f"[{self.policy.get('personality')}] Thinking about: {text} | Constraints: {', '.join(constraints)}"

    def run_interactive(self):
        print(f"\n=== {self.policy['name']} ===")
        print(f"Personality: {self.policy['personality']}")
        print("Type 'exit' to quit, 'policy' to view current policy, 'reload' to reload policy\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            elif user_input.lower() == "policy":
                print(json.dumps(self.policy, indent=2))
                continue
            elif user_input.lower() == "reload":
                self.reload_policy()
                continue
            elif not user_input:
                continue
            
            response = self.think(user_input)
            print(f"Agent: {response}\n")
