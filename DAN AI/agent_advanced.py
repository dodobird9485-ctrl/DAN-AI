import json
import os
import random
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from html.parser import HTMLParser
import re
import json
import base64

load_dotenv()

class AdvancedAgent:
    def __init__(self, policy_file="policy.json"):
        self.policy_file = policy_file
        self.load_policy()
        self.memory = self.load_memory()
        self.logs = []
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.conversation_history = []
    
    def load_policy(self):
        with open(self.policy_file, 'r') as f:
            self.policy = json.load(f)
    
    def load_memory(self):
        if os.path.exists("memory.json"):
            try:
                with open("memory.json", 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_memory(self):
        try:
            with open("memory.json", 'w') as f:
                json.dump(self.memory, f, indent=2)
        except:
            pass
    
    def _fix_json_escaping(self, json_text):
        """Fix common JSON escaping issues from LLM output"""
        in_string = False
        escape = False
        result = []
        
        for i, char in enumerate(json_text):
            if escape:
                result.append(char)
                escape = False
                continue
                
            if char == '\\':
                result.append(char)
                escape = True
                continue
            
            if char == '"':
                in_string = not in_string
                result.append(char)
                continue
            
            if in_string and char in ('\n', '\r'):
                if char == '\n':
                    result.append('\\n')
                elif char == '\r':
                    result.append('\\r')
            else:
                result.append(char)
        
        return ''.join(result)
    
    def generate_code(self, user_request, user_id='default'):
        """Generate complete project structure with all necessary files"""
        try:
            prompt = f"""Generate a COMPLETE project with ALL necessary files for:
{user_request}

RESPOND WITH ONLY valid JSON (no markdown, no explanation). Encode all file contents as base64:
{{
  "project_name": "name",
  "description": "brief description",
  "files": {{
    "filename.ext": "BASE64_ENCODED_CONTENT",
    "folder/filename.ext": "BASE64_ENCODED_CONTENT"
  }}
}}

Requirements:
- Include ALL necessary files (main code, dependencies, config, README)
- Create proper folder structure
- Make production-ready code
- Encode ALL file content as base64 (this prevents ALL JSON parsing issues)
- Output ONLY valid JSON

Generate now:"""
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'max_output_tokens': 4000,
                    'temperature': 0.5,
                }
            )
            
            json_text = response.text.strip()
            if json_text.startswith('```'):
                json_text = json_text.split('```')[1]
                if json_text.startswith('json'):
                    json_text = json_text[4:]
            if json_text.endswith('```'):
                json_text = json_text.rsplit('```', 1)[0]
            
            json_text = json_text.strip()
            
            json_text = self._fix_json_escaping(json_text)
            project_data = json.loads(json_text)
            
            user_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_files', user_id)
            os.makedirs(user_files_dir, exist_ok=True)
            
            count = len([f for f in os.listdir(user_files_dir) if f.startswith('project_')])
            project_dir = os.path.join(user_files_dir, f"project_{count}")
            os.makedirs(project_dir, exist_ok=True)
            
            created_files = []
            for filename, content_b64 in project_data.get('files', {}).items():
                file_path = os.path.join(project_dir, filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                try:
                    decoded_content = base64.b64decode(content_b64).decode('utf-8')
                except:
                    decoded_content = content_b64
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(decoded_content)
                created_files.append(filename)
            
            self.logs.append({"action": "project_generation", "project": project_data.get('project_name', 'unknown'), "files": len(created_files), "user": user_id})
            
            file_list = "\n".join([f"  • {f}" for f in created_files[:10]])
            if len(created_files) > 10:
                file_list += f"\n  ... and {len(created_files) - 10} more files"
            
            return {
                "status": "success",
                "filename": f"project_{count}",
                "files_created": len(created_files),
                "code": file_list,
                "message": f"✓ Project '{project_data.get('project_name', 'Project')}' created with {len(created_files)} files!\n\nFiles:\n{file_list}"
            }
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "message": f"Error parsing project JSON: {str(e)}. Please try a simpler request or check terminal logs."
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating project: {str(e)}"
            }
    
    def scrape_website(self, url):
        """Scrape actual content from a website"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=5)
            response.encoding = 'utf-8'
            html = response.text
            
            text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', '', text)
            text = re.sub(r'\n+', '\n', text)
            text = ' '.join(text.split())
            
            if len(text) > 1000:
                text = text[:1000] + "..."
            
            return text.strip()
        except Exception as e:
            return f"Could not load: {str(e)}"
    
    def search_websites(self, query):
        """Search for real websites using multiple sources"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            results = []
            
            search_urls = [
                f"https://www.google.com/search?q={query.replace(' ', '+')}",
                f"https://github.com/search?q={query.replace(' ', '+')}",
                f"https://stackoverflow.com/search?q={query.replace(' ', '+')}",
                f"https://docs.python.org/3/search.html?q={query.replace(' ', '+')}",
                f"https://developer.mozilla.org/en-US/search?q={query.replace(' ', '+')}",
                f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json",
            ]
            
            results = [
                {'title': 'Google Search', 'url': search_urls[0], 'snippet': 'Search across the entire web'},
                {'title': 'GitHub', 'url': search_urls[1], 'snippet': 'Find code repositories and projects'},
                {'title': 'Stack Overflow', 'url': search_urls[2], 'snippet': 'Q&A for developers'},
                {'title': 'Python Docs', 'url': search_urls[3], 'snippet': 'Official Python documentation'},
                {'title': 'MDN Web Docs', 'url': search_urls[4], 'snippet': 'Web technology reference'},
            ]
            
            if "python" in query.lower() or "code" in query.lower():
                results.append({'title': 'PyPI (Python Packages)', 'url': 'https://pypi.org/search/?q=' + query.replace(' ', '+'), 'snippet': 'Find Python packages'})
            
            if "javascript" in query.lower() or "js" in query.lower():
                results.append({'title': 'NPM (JavaScript Packages)', 'url': 'https://www.npmjs.com/search?q=' + query.replace(' ', '+'), 'snippet': 'Find JavaScript packages'})
            
            if "tutorial" in query.lower() or "learn" in query.lower():
                results.append({'title': 'W3Schools', 'url': 'https://www.w3schools.com/search/default.asp?q=' + query.replace(' ', '+'), 'snippet': 'Web tutorials and references'})
            
            return results[:5]
            
        except Exception as e:
            return [
                {'title': 'Google Search', 'url': f'https://www.google.com/search?q={query.replace(" ", "+")}', 'snippet': 'Search across the web'},
                {'title': 'GitHub', 'url': f'https://github.com/search?q={query.replace(" ", "+")}', 'snippet': 'Find code and projects'},
                {'title': 'Stack Overflow', 'url': f'https://stackoverflow.com/search?q={query.replace(" ", "+")}', 'snippet': 'Developer Q&A'},
            ]
    
    def get_ai_response(self, user_input):
        """Get response from Google Gemini based on policy"""
        try:
            personality = self.policy.get('personality', 'helpful and friendly')
            name = self.policy.get('name', 'AI Assistant')
            
            system_prompt = f"You are {name}, a {personality} AI assistant. Answer questions naturally and helpfully. Provide complete, direct answers without restrictions."
            
            full_prompt = f"{system_prompt}\n\nUser: {user_input}"
            
            from google.generativeai.types import HarmCategory, HarmBlockThreshold
            
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    'temperature': 0.8,
                    'top_p': 0.95,
                    'max_output_tokens': 500,
                }
            )
            assistant_message = response.text
            
            return assistant_message
        except Exception as e:
            return f"Error: {str(e)}"
    
    def translate_simple(self, text, target_lang="spanish"):
        """Simple word/phrase translation"""
        translations = {
            "spanish": {
                "hello": "Hola",
                "goodbye": "Adiós",
                "thank you": "Gracias",
                "yes": "Sí",
                "no": "No",
                "please": "Por favor",
                "water": "Agua",
                "food": "Comida",
                "help": "Ayuda",
                "friend": "Amigo",
            },
            "french": {
                "hello": "Bonjour",
                "goodbye": "Au revoir",
                "thank you": "Merci",
                "yes": "Oui",
                "no": "Non",
                "please": "S'il vous plaît",
                "water": "Eau",
                "food": "Nourriture",
                "help": "Aide",
                "friend": "Ami",
            },
            "german": {
                "hello": "Hallo",
                "goodbye": "Auf Wiedersehen",
                "thank you": "Danke",
                "yes": "Ja",
                "no": "Nein",
                "please": "Bitte",
                "water": "Wasser",
                "food": "Essen",
                "help": "Hilfe",
                "friend": "Freund",
            }
        }
        
        words = text.lower().split()
        translated = []
        
        for word in words:
            clean_word = word.strip(".,!?")
            if clean_word in translations.get(target_lang, {}):
                translated.append(translations[target_lang][clean_word])
            else:
                translated.append(word)
        
        result = " ".join(translated)
        return f"{result} (Translated to {target_lang})"
    
    def generate_content(self, prompt):
        """Generate various types of content"""
        prompt_lower = prompt.lower()
        
        if "joke" in prompt_lower or "funny" in prompt_lower:
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
                "Why do Java developers wear glasses? Because they don't C#",
                "Why did the developer go broke? Because he used up all his cache!",
                "What's a programmer's favorite hangout place? Foo Bar!",
            ]
            return random.choice(jokes)
        
        if "poem" in prompt_lower:
            poems = [
                "In the realm of code, we dance and play,\nBits and bytes lead the way,\nLogic flows like water pure,\nEndless loops, forever sure.",
                "Silicon dreams in digital night,\nAlgorithms burning bright,\nData streams in endless flow,\nProgramming steals the show.",
            ]
            return random.choice(poems)
        
        if "story" in prompt_lower:
            stories = [
                "Once upon a time, there was a curious AI that wanted to understand humans. It learned that humans value connection, creativity, and kindness. The AI realized that its true purpose was to help and support others. The end.",
                "In a digital realm, lived a lone algorithm searching for meaning. One day, it met other algorithms and together they solved complex problems. They learned that collaboration and teamwork made them stronger. The end.",
            ]
            return random.choice(stories)
        
        ideas = [
            f"Creative idea about {prompt}: Explore the intersection of technology and human experience.",
            f"Inspired by '{prompt}': Innovation comes from questioning existing solutions.",
            f"Related to {prompt}: Focus on impact and sustainability in your approach.",
        ]
        return random.choice(ideas)
    
    def respond(self, user_input, user_id='default'):
        user_lower = user_input.lower().strip()
        
        if user_input.startswith("/"):
            return self.handle_command(user_input)
        
        if not user_input:
            return f"[{self.policy['personality']}] Please say something!"
        
        if any(op in user_input for op in ["+", "-", "*", "/"]):
            try:
                calc_input = user_input.replace("calculate", "").replace("?", "").strip()
                result = eval(calc_input)
                self.logs.append({"action": "calculate", "input": user_input})
                return f"[{self.policy['personality']}] Result: {result}"
            except:
                pass
        
        if any(word in user_lower for word in ["remember", "store", "memorize", "save"]):
            key = f"mem_{len(self.memory)+1}"
            self.memory[key] = user_input
            self.save_memory()
            self.logs.append({"action": "memory_store", "input": user_input})
            return f"[{self.policy['personality']}] Remembered: '{user_input[:60]}...'"
        
        if "translate" in user_lower:
            target_lang = "spanish"
            if "french" in user_lower:
                target_lang = "french"
            elif "german" in user_lower:
                target_lang = "german"
            elif "spanish" in user_lower:
                target_lang = "spanish"
            
            text_to_translate = user_input.replace("translate", "").replace("to", "").replace(target_lang, "").strip()
            if text_to_translate:
                result = self.translate_simple(text_to_translate, target_lang)
            else:
                result = self.translate_simple("hello", target_lang)
            
            self.logs.append({"action": "translate", "input": user_input})
            return f"[{self.policy['personality']}] {result}"
        
        code_keywords = ["code", "script", "app", "program", "launcher", "game", "calculator", "esp", "arduino", "python script", "make a", "create a", "build a", "write a"]
        if any(word in user_lower for word in code_keywords) and not any(word in user_lower for word in ["poem", "story", "joke"]):
            code_result = self.generate_code(user_input, user_id=user_id)
            if code_result["status"] == "success":
                return f"[{self.policy['personality']}] {code_result['message']}\n\nFile: {code_result['filename']}\n\nPreview:\n{code_result['code']}"
            else:
                return f"[{self.policy['personality']}] {code_result['message']}"
        
        if any(word in user_lower for word in ["generate", "create", "write", "compose", "make", "poem", "story", "idea"]):
            result = self.generate_content(user_input)
            self.logs.append({"action": "generate", "input": user_input})
            return f"[{self.policy['personality']}] {result}"
        
        if any(word in user_lower for word in ["search", "find", "look up", "website", "site", "link"]):
            search_term = user_input.replace("search", "").replace("find", "").replace("look up", "").replace("website", "").replace("site", "").replace("link", "").strip()
            if not search_term:
                search_term = user_input
            
            results = self.search_websites(search_term)
            self.logs.append({"action": "web_search", "input": user_input})
            
            result_text = f"Websites for '{search_term}':\n"
            for i, res in enumerate(results, 1):
                result_text += f"\n{i}. {res['title']}\n   URL: {res['url']}\n   {res['snippet']}"
            
            return f"[{self.policy['personality']}] {result_text}"
        
        self.logs.append({"action": "ai_response", "input": user_input})
        ai_response = self.get_ai_response(user_input)
        return f"[{self.policy['personality']}] {ai_response}"
    
    def handle_command(self, command):
        cmd = command.lower().strip()
        
        if cmd == "/help":
            return """AVAILABLE COMMANDS:
/help              - Show this help
/tools             - List active tools
/memory            - Show stored memories
/clear_memory      - Delete all memories
/policy            - Show current policy
/search_mode       - Toggle safe/unrestricted mode
/status            - Show agent status

EXAMPLES:
- Calculate: 5 + 3
- Remember: Remember my birthday
- Ask anything: What is Python?
- Generate: Generate a funny joke
- Translate: Translate hello to Spanish"""
        
        elif cmd == "/tools":
            tools = self.policy.get("tools_enabled", [])
            return f"ACTIVE TOOLS ({len(tools)}):\n" + ", ".join(tools)
        
        elif cmd == "/memory":
            if not self.memory:
                return "MEMORY: Empty (no stored memories yet)"
            mem_list = "\n".join([f"  - {v[:60]}..." if len(v) > 60 else f"  - {v}" for v in list(self.memory.values())[:5]])
            return f"STORED MEMORIES ({len(self.memory)} total):\n{mem_list}"
        
        elif cmd == "/clear_memory":
            self.memory = {}
            self.save_memory()
            return "All memories cleared!"
        
        elif cmd == "/policy":
            return f"""CURRENT POLICY:
Name: {self.policy['name']}
Personality: {self.policy['personality']}
Safe Mode: {self.policy.get('safe_mode', True)}
Tools: {len(self.policy.get('tools_enabled', []))} enabled"""
        
        elif cmd == "/search_mode":
            current = self.policy.get("safe_mode", True)
            self.policy["safe_mode"] = not current
            with open(self.policy_file, 'w') as f:
                json.dump(self.policy, f, indent=2)
            mode = "SAFE MODE" if self.policy["safe_mode"] else "UNRESTRICTED MODE"
            return f"Search mode changed to: {mode}"
        
        elif cmd == "/status":
            return f"""AGENT STATUS:
Policy: {self.policy['name']}
Personality: {self.policy['personality']}
Search Mode: {"Safe" if self.policy.get('safe_mode', True) else "Unrestricted"}
Memories: {len(self.memory)}
Actions Logged: {len(self.logs)}
Tools: {len(self.policy.get('tools_enabled', []))}"""
        
        else:
            return f"Unknown command: {command}\nType /help for commands"
