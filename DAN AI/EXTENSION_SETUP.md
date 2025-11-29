# DAN AI Agent VS Code Extension - Setup Guide

## Fixed Issues
✓ Added proper node-fetch import for API calls
✓ Improved error handling and response parsing
✓ Enhanced UI with VS Code theme integration
✓ Added status bar button for quick access ($(sparkle) DAN AI)
✓ Added keyboard shortcut: **Ctrl+Shift+A** (Windows/Linux) or **Cmd+Shift+A** (Mac)
✓ Added error message styling
✓ Improved message formatting with word wrapping

## Installation

### Prerequisites
- Node.js 12+ and npm installed
- VS Code 1.70 or later

### Steps

1. **Install dependencies** (first time only):
```bash
cd "c:\Users\Noah Taylor\Downloads\DAN AI"
npm install
```

2. **Open the extension development environment in VS Code**:
   - Open this folder in VS Code
   - Press `F5` to open VS Code Extension Development Host

3. **Start Flask backend** (in a separate terminal):
```bash
python app.py
```

The Flask app will run on http://localhost:5000

## Usage

Once installed and Flask is running:

### Option 1: Keyboard Shortcut
- Windows/Linux: Press **Ctrl+Shift+A**
- Mac: Press **Cmd+Shift+A**

### Option 2: Status Bar
- Click the **$(sparkle) DAN AI** button in the status bar (bottom right)

### Option 3: Command Palette
- Press Ctrl+Shift+P (Windows/Linux) or Cmd+Shift+P (Mac)
- Type "Open DAN AI Agent"
- Press Enter

## Features
- 💬 Chat with AI (Gemini-powered)
- 🔍 Search the web
- 💾 Store memories
- 🧮 Perform calculations
- 📝 Generate code
- 🌍 Web scraping
- 🗣️ Translation

## Architecture
- **Frontend**: VS Code Webview (HTML/CSS/JavaScript)
- **Backend**: Python Flask + Google Gemini API
- **Communication**: VS Code Message API + HTTP fetch

## Troubleshooting

### "Cannot connect to agent" error
- Make sure Flask is running: `python app.py`
- Check that port 5000 is not blocked
- Ensure `.env` file has valid Google API key

### Extension not loading
- Press Ctrl+Shift+P and run "Developer: Reload Window"
- Check extension console (Help → Toggle Developer Tools)

### Dependencies not installing
If npm installation fails:
1. Install Node.js from https://nodejs.org/
2. Open new terminal
3. Run `npm install` again

## Publishing (Optional)
To publish to VS Code Marketplace:
```bash
npm install -g vsce
vsce publish
```
