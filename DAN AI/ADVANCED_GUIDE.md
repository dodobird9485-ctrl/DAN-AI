# AI Agent - Advanced Features Guide

## Features Included ✅

### 1. **Web Search**
- **Safe Mode (Default)**: Searches only trusted sites
  - Wikipedia, GitHub, Stack Overflow, Python Docs, MDN
  - Perfect for learning and development
  - No malicious content
  
- **Unrestricted Mode**: Searches full web via DuckDuckGo
  - Access to all web content
  - Toggle with "🔒 Toggle Search" button

**How to Use:**
- Type any question: `What is machine learning?`
- Use search keyword: `Search for python tutorials`
- Agent automatically detects questions (has ?)

### 2. **Persistent Memory**
Agent remembers what you tell it!

**Store:**
- `Remember my favorite color is blue`
- `Store my email as john@example.com`

**View:** Sidebar shows last 5 memories

**Clear:** Click "🗑️ Clear Mem" button (or use `/clear_memory`)

### 3. **Real Tool Implementations**

| Tool | Usage | Example |
|------|-------|---------|
| calculate | Math operations | `5 + 3`, `100 * 2` |
| memory | Store/recall info | `Remember my birthday` |
| translate | Language conversion | `Translate hello to Spanish` |
| generate | Create content | `Generate a funny poem` |
| web_search | Search the web | `What is AI?` or `Search for...` |
| search | Find information | `Who invented the internet?` |

### 4. **Command System**
Type commands starting with `/`:

```
/help              - Show all available commands
/tools             - List active tools
/memory            - View stored memories
/clear_memory      - Delete all memories
/policy            - Show current policy settings
/search_mode       - Toggle safe/unrestricted mode
/status            - Show agent statistics
```

### 5. **Persistent Logging**
All actions are logged and appear in "Recent Actions" sidebar:
- calculate
- memory_store
- web_search
- translate
- generate
- question
- acknowledge

### 6. **Beautiful UI**
- Modern gradient design
- Real-time stats
- Smooth animations
- Responsive layout
- Dark/light-friendly colors

---

## Configuration

### Change Search Safety

**In Web Interface:**
1. Click "🔒 Toggle Search" button
2. Mode shows as green (Safe) or yellow (Unrestricted)

**In Code:**
Edit `policy.json`:
```json
"safe_mode": true   // or false for unrestricted
```

### Customize Agent Personality

Edit `policy.json`:
```json
{
  "name": "My Custom Agent",
  "personality": "funny and playful",
  "goals": ["make jokes", "be helpful"],
  "constraints": ["keep it appropriate"],
  "safe_mode": true,
  "tools_enabled": ["calculate", "generate", "web_search"]
}
```

### Available Policies (in `policy.json`)

**Smart Assistant (Default)**
- Helpful, friendly, general purpose
- All tools enabled
- Safe mode on

**Funny Bot**
```json
{
  "name": "Funny Bot",
  "personality": "funny and playful",
  "goals": ["make jokes", "entertain"],
  "constraints": ["keep it clean"],
  "tools_enabled": ["generate", "web_search", "memory"]
}
```

**Data Analyst**
```json
{
  "name": "Data Analyst",
  "personality": "analytical and precise",
  "goals": ["analyze data", "extract insights"],
  "tools_enabled": ["calculate", "statistics", "validate"]
}
```

**Developer Helper**
```json
{
  "name": "Developer Helper",
  "personality": "technical and helpful",
  "goals": ["help with code", "solve problems"],
  "tools_enabled": ["calculate", "web_search", "memory"]
}
```

---

## Usage Examples

### Example 1: Learning with Safe Search
```
You: What is quantum computing?
Agent: Searches Wikipedia and returns safe, educational info
```

### Example 2: Storing & Recalling
```
You: Remember my birthday is December 25
Agent: ✓ Remembered!

Later...
You: /memory
Agent: Shows all stored memories
```

### Example 3: Generating Content
```
You: Generate a short story about AI
Agent: Creates creative content based on your request
```

### Example 4: Switching Search Modes
```
You: Toggle Search Mode (click button)
Agent: Switches from Safe to Unrestricted or vice versa

You: Search for advanced AI papers
Agent: (In unrestricted mode) Searches full web
```

### Example 5: Using Commands
```
You: /status
Agent: Shows policy, memory count, tools, search mode
```

---

## File Structure

```
DAN AI/
├── agent_advanced.py      # Advanced agent with web search
├── app.py                 # Flask web server (updated)
├── policy.json            # Configuration (has safe_mode)
├── memory.json            # Persistent memory storage
├── requirements.txt       # Updated with requests
├── templates/
│   └── index.html        # Improved UI with new features
├── START.bat             # Quick start
└── ADVANCED_GUIDE.md     # This file
```

---

## How It Works

### Safe Mode (default)
1. User asks question
2. Agent detects it's a search
3. Adds search to trusted sites only
4. Uses DuckDuckGo API with site filters
5. Returns safe, relevant results

### Unrestricted Mode
1. User toggles via button
2. safe_mode = false in policy.json
3. Agent searches full web via DuckDuckGo
4. All results included
5. User can toggle back anytime

### Memory Storage
1. User says "Remember X"
2. Agent saves to memory dict
3. `memory.json` automatically saved
4. On restart, memory is loaded
5. User can view/clear anytime

---

## Troubleshooting

**Q: Web search not working?**
- A: Make sure requests library is installed: `pip install requests`
- Check internet connection
- Try different search query

**Q: Memory not persisting?**
- A: Make sure `memory.json` can be created
- Check folder permissions
- Restart the agent

**Q: Safe mode not filtering?**
- A: Safe mode uses trusted sites, some results may not be perfect
- Toggle to unrestricted if needed
- Or try more specific search term

**Q: Agent gives empty responses?**
- A: Message might not trigger any tool
- Try using /help for command list
- Add more keywords to your message

---

## Tips

1. **Combine features**: Search → Remember → Generate
   ```
   What is Python?
   Remember Python is a programming language
   Generate a Python joke
   ```

2. **Use commands for info**: Type `/status` to see everything

3. **Toggle search modes** based on what you need:
   - Safe for learning
   - Unrestricted for full research

4. **Clear memory** when starting fresh: `Clear Mem` button

5. **Check recent actions** sidebar to see what agent is doing

---

## Advanced: Custom Configuration

Create custom policies by editing `policy.json`:

```json
{
  "name": "Research Assistant",
  "personality": "scholarly and thorough",
  "goals": [
    "find accurate information",
    "provide citations",
    "help with research"
  ],
  "constraints": [
    "verify sources",
    "avoid speculation"
  ],
  "safe_mode": true,
  "tools_enabled": [
    "web_search",
    "memory",
    "extract"
  ]
}
```

After editing, click **Reload** in web interface (or restart agent).

---

Enjoy your AI Agent! 🚀
