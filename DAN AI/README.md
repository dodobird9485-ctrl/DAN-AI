# AI Agent with Changeable Policy

A flexible AI agent with 23 tools and a changeable policy system. Now with a beautiful web interface!

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Web Interface
**Double-click:** `START.bat`

Or from command line:
```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

## What You Get

### Web Interface
- 💬 Real-time chat with the agent
- 📊 Live stats (memory, audit logs, requests)
- 🛠️ Active tools display
- 💾 Memory viewer
- 📝 Audit log viewer
- 🔄 Reload policy button

### 23 Built-in Tools
- **calculate** - Math operations
- **memory** - Store/recall data
- **logic** - Conditional reasoning
- **classify** - Categorize input
- **summarize** - Condense text
- **sentiment** - Emotional analysis
- **fetch_url** - Get web data
- **database** - Query data
- **api_call** - Call APIs
- **file_io** - Read/write files
- **translate** - Language conversion
- **extract** - Pull structured data
- **generate** - Create content
- **parse_json** - Handle JSON
- **statistics** - Calculate metrics
- **validate** - Check validity
- **compare** - Analyze differences
- **execute_code** - Run scripts
- **schedule** - Plan tasks
- **audit** - Log activities
- **rate_limit** - Control requests
- **search** - Find information
- **reason** - Logical reasoning

## Change Agent Behavior

Edit **`policy.json`**:
```json
{
  "name": "My Agent",
  "personality": "helpful and friendly",
  "goals": ["assist users", "provide info"],
  "constraints": ["be respectful"],
  "max_steps": 5,
  "verbose": true,
  "tools_enabled": ["calculate", "memory", "translate"]
}
```

Click **🔄 Reload** in the web interface to apply changes.

## Example Policies

See `policy_examples.json` for:
- Minimal Policy
- Data Analyst Policy
- Creative Policy
- Developer Policy
- Admin Policy

## File Structure
```
DAN AI/
├── app.py              # Flask web server
├── agent.py            # Core agent logic
├── policy.json         # Current policy config
├── policy_examples.json # Example policies
├── requirements.txt    # Python dependencies
├── START.bat          # Quick start script
├── templates/
│   └── index.html     # Web interface
├── test.py            # Test suite
├── demo.py            # Demo scenarios
├── TOOLS.md           # Tools reference
└── README.md          # This file
```

## Usage Examples

In the web interface, try:
- `Calculate 10 + 5`
- `Remember my favorite color is blue`
- `Translate to Spanish`
- `Generate a poem`
- `Classify this request`
- `Validate this data`
- `What is sentiment analysis?`

## Tips

1. **Change personality** → Edit policy.json and reload
2. **Enable/disable tools** → Edit `tools_enabled` array in policy.json
3. **View memory** → Check "💾 Memory" sidebar
4. **Check audit log** → See "📝 Recent Audit" sidebar
5. **Create custom policy** → Copy from `policy_examples.json`

## Troubleshooting

**Flask not found?**
```bash
pip install Flask
```

**Port 5000 already in use?**
Edit `app.py` line 48: `app.run(debug=True, port=5001)`

**Agent not responding?**
Make sure `policy.json` exists in the same folder as `app.py`

---

**Enjoy your customizable AI agent!** 🤖
