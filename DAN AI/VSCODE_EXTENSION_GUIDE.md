# DAN AI Coding Suite - VS Code Extension Guide

## Overview
The enhanced VS Code extension now provides a **complete coding environment** with file management, code editing, terminal access, and AI assistance—all integrated into VS Code.

## Features

### 1. **File Explorer** 📁
- **Browse project structure**: Navigate your entire project tree
- **Click to open**: Select any file to view its contents
- **Nested folders**: See folder hierarchy up to 3 levels deep
- **Ignored files**: Automatically hides node_modules, .git, __pycache__, etc.

**How to use:**
1. Open extension (Ctrl+Shift+A)
2. Go to "📁 Files" tab in sidebar
3. Click any file to open and view it

### 2. **Code Editor** 📝
- **Syntax highlighting**: Automatic highlighting for Python, JavaScript, HTML, C++, Java, etc.
- **View files**: Read file contents with proper formatting
- **Edit files**: Make changes to any file
- **Save changes**: Click "💾 Save" to write changes back to disk

**Action buttons:**
- **💾 Save** - Save current file
- **🗑️ Delete** - Remove file from disk
- **▶ Run File** - Execute Python/JavaScript files directly

### 3. **Terminal** 💻
- **Command execution**: Run any shell command
- **Real-time output**: See command results immediately
- **Color-coded**: Success (green), Error (red), Normal (white)
- **Working directory**: All commands run in project root

**Supported commands:**
```bash
# Python
python script.py
python -m pip install package

# Node.js
node script.js
npm install

# System
mkdir folder_name
dir (Windows) or ls (Mac/Linux)
git status
pip list
```

**How to use:**
1. Click "Terminal" tab
2. Type command in input box
3. Press Enter or click "Execute"
4. View results in output area

### 4. **File Operations** 📂
Access via "⚙️ Commands" tab in sidebar:

- **+ New File** - Create a new file
  - Prompts for filename (e.g., `script.py`, `index.html`)
  - Creates empty file in project root

- **+ New Folder** - Create a new directory
  - Prompts for folder name
  - Creates directory in project root

- **▶ Run Command** - Quick access to terminal
  - Switches to Terminal tab
  - Auto-focuses input field

- **🔨 Build** - Build/compile project
  - Runs project build scripts
  - Shows output in terminal

### 5. **Code Execution** ▶️
Run files directly from the Code Editor:

**Python files (.py):**
```bash
# Click "▶ Run File" to execute
python your_script.py
```

**JavaScript files (.js):**
```bash
# Requires Node.js installed
node your_script.js
```

**HTML files (.html):**
- Click "▶ Run File" for instructions
- Right-click file in VS Code explorer and "Open with Default Browser"

### 6. **AI Chat** 🤖
- **Ask questions**: Get AI responses to any query
- **Code generation**: Ask for code in any language
- **Web search**: "Search for..." queries
- **Explanations**: Get help understanding code

**Example prompts:**
- "Create a Python calculator"
- "Explain this code: [paste code]"
- "Search for Python tutorials"
- "Generate a Node.js web server"

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl+Shift+A** | Open/Focus DAN AI extension |
| **Cmd+Shift+A** | macOS equivalent |
| **Enter** (in any input) | Send command/message |
| **Ctrl+C** (in terminal) | Cancel long-running command |

---

## Setup & Installation

### Prerequisites
```bash
# Required
- Node.js 12+ (includes npm)
- Python 3.7+
- VS Code 1.70+
```

### Installation Steps

**Step 1:** Install dependencies
```bash
cd "c:\Users\Noah Taylor\Downloads\DAN AI"
npm install
```

**Step 2:** Open in VS Code
- Open this folder in VS Code
- Press `F5` to start Extension Development Host

**Step 3:** Start Flask backend
```bash
python app.py
```

Flask will run on `http://localhost:5000`

**Step 4:** Open extension
- Press `Ctrl+Shift+A` in VS Code
- Click the "$(sparkle) DAN Code" button in status bar (bottom right)

---

## Complete Feature Set

```
┌─────────────────────────────────────┐
│     DAN AI Coding Suite             │
├──────────────┬──────────────────────┤
│ 📁 Files     │  Code Editor         │
│ ⚙️ Commands  │  ▶ Run File          │
│              │  💾 Save             │
│              │  🗑️ Delete           │
├──────────────┴──────────────────────┤
│  Tabs:                               │
│  • Code Editor - View/Edit files     │
│  • Terminal - Execute commands       │
│  • Chat - AI Assistant               │
└─────────────────────────────────────┘
```

### Sidebar - Files Tab
- Browse all project files
- Click any file to view it
- Auto-loads directory structure

### Sidebar - Commands Tab
- **+ New File** → Create empty file
- **+ New Folder** → Create directory
- **▶ Run Command** → Open terminal
- **🔨 Build** → Build project

### Main Editor Tab
- **Code Editor**: View/edit files with syntax highlighting
- **Terminal**: Execute commands with color-coded output
- **Chat**: Ask AI for help, code, searches

---

## Common Workflows

### Workflow 1: Create and Run a Python Script
```
1. Click "⚙️ Commands" → "+ New File"
2. Enter: calculator.py
3. File appears in editor
4. Type your Python code
5. Click "💾 Save"
6. Click "▶ Run File"
7. See output in Terminal tab
```

### Workflow 2: Execute Multiple Commands
```
1. Click "Terminal" tab
2. Type: pip install requests
3. Press Enter
4. Type: python script.py
5. Press Enter
6. View results
```

### Workflow 3: Use AI to Generate Code
```
1. Click "Chat" tab
2. Type: "Create a Python function to reverse a string"
3. AI generates code
4. Copy generated code
5. Create new file via Commands
6. Paste code
7. Save and run
```

### Workflow 4: Edit Existing Project File
```
1. Click "📁 Files" tab
2. Click file name (e.g., app.py)
3. View contents in editor
4. Make changes
5. Click "💾 Save"
```

---

## File Operations API

The extension uses these backend endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/project_files` | GET | List project structure |
| `/api/read_file` | POST | Read file contents |
| `/api/write_file` | POST | Save file contents |
| `/api/delete_file` | POST | Delete a file |
| `/api/create_file` | POST | Create new file |
| `/api/run_file` | POST | Execute Python/JS file |
| `/api/execute_cmd` | POST | Run shell command |
| `/api/build` | POST | Build project |
| `/api/think` | POST | AI chat endpoint |

---

## Security Notes

✅ **Safe operations:**
- All file paths validated within project root
- Dangerous commands blocked (`rm -rf`, `del /s`, etc.)
- Command execution has 10-second timeout
- File operations restricted to project directory

⚠️ **Be careful with:**
- Running untrusted code
- Executing system commands
- Large file operations (limited to 10s timeout)

---

## Troubleshooting

### "Cannot connect to agent" Error
```
✓ Make sure Flask is running: python app.py
✓ Check that port 5000 is not blocked
✓ Verify .env file has valid Google API key
✓ Restart extension (Ctrl+Shift+P → Reload Window)
```

### Files not appearing in Explorer
```
✓ Click "⚙️ Commands" tab, then back to "📁 Files"
✓ Refresh file list
✓ Check file is in project root or subdirectories
```

### Commands not executing
```
✓ Ensure command is valid for your OS
✓ Check Python/Node.js paths are in system PATH
✓ Commands must complete within 10 seconds
```

### Code highlighting not working
```
✓ File must have proper extension (.py, .js, .html, etc.)
✓ Try clicking a different file, then back
✓ Reload extension
```

---

## Tips & Tricks

💡 **Pro Tips:**
- Use terminal for git commands: `git status`, `git commit`, etc.
- Create test files quickly with "New File" button
- Ask AI to generate project structure
- Use ▶ Run File to test scripts immediately
- Terminal shows full command output for debugging

🎯 **Best Practices:**
- Save files frequently (Ctrl+S habit)
- Test small code snippets before large changes
- Use Chat tab to understand errors
- Keep working files in project root for easy access
- Use terminal for version control and package management

---

## Keyboard Reference

When in Code Editor:
- **Ctrl+A** - Select all text (view-only)
- **Ctrl+C** - Copy text

When in Terminal:
- **Ctrl+C** - Cancel running command
- **Enter** - Execute command
- **Up/Down arrows** - Command history (if supported)

When in Chat:
- **Enter** - Send message
- **Shift+Enter** - New line in message

---

## Getting Help

**Inside the extension:**
- Chat tab: Ask AI directly
- Example: "How do I use this feature?"

**Reference:**
- Python: Ask "python syntax help"
- JavaScript: Ask "javascript example"
- Commands: Ask "bash command help"

**Emergency restart:**
1. Close extension panel
2. Ctrl+Shift+P → "Reload Window"
3. Reopen extension

---

## Next Steps

1. **Install dependencies** (if not done): `npm install`
2. **Start Flask backend**: `python app.py`
3. **Open VS Code**: Open project folder
4. **Press F5**: Launch Extension Dev Host
5. **Press Ctrl+Shift+A**: Open DAN AI Coding Suite
6. **Start creating & coding!**

Enjoy your AI-powered coding experience! 🚀
