# VS Code Extension Setup

To run the DAN AI Agent as a VS Code extension:

## Prerequisites
- Node.js (download from nodejs.org)
- npm (comes with Node.js)
- VS Code

## Installation

### 1. Install Node.js dependencies
```bash
npm install
```

### 2. Run the Flask backend
Keep the Python app running in another terminal:
```bash
python app.py
```
(This starts the agent on http://localhost:5000)

### 3. Run extension in development mode
```bash
npm run watch
```

### 4. Open VS Code Extension Host
- Press `F5` in VS Code (with this folder open)
- A new VS Code window will open with the extension loaded
- Look for "DAN AI Agent" in the Explorer sidebar

## Features
- Chat interface in VS Code sidebar
- Code generation (ask "create a python calculator")
- Web search (ask "search Python tutorials")
- Memory storage
- Policy-based responses

## Building for distribution
```bash
npm install -g vsce
vsce package
```

This creates a `.vsix` file you can share or install locally.

## Troubleshooting
- Make sure Flask app is running on port 5000
- If extension doesn't appear, reload VS Code window (Cmd+R / Ctrl+Shift+R)
- Check VS Code's Developer Console for errors (Help → Toggle Developer Tools)
