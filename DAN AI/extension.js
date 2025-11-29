const vscode = require('vscode');
const fetch = require('node-fetch');

const API_URL = 'http://localhost:5000/api';
let currentPanel;
let currentFile = null;

async function apiCall(endpoint, method = 'GET', body = null) {
    try {
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        if (body) options.body = JSON.stringify(body);
        
        const response = await fetch(`${API_URL}${endpoint}`, options);
        if (!response.ok) {
            return { error: `Server error: ${response.statusText}` };
        }
        return await response.json();
    } catch (error) {
        return { error: 'API Error: ' + error.message };
    }
}

function getWebviewContent() {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DAN AI Coding Suite</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--vscode-editor-background);
            color: var(--vscode-editor-foreground);
            height: 100vh;
            overflow: hidden;
        }
        .main-container {
            display: flex;
            height: 100vh;
            gap: 0;
        }
        .sidebar {
            width: 250px;
            background: var(--vscode-sideBar-background);
            border-right: 1px solid var(--vscode-panel-border);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .sidebar-tabs {
            display: flex;
            background: var(--vscode-sideBar-background);
            border-bottom: 1px solid var(--vscode-panel-border);
        }
        .sidebar-tab {
            flex: 1;
            padding: 8px;
            background: transparent;
            color: var(--vscode-sideBarTitle-foreground);
            border: none;
            cursor: pointer;
            text-align: center;
            font-size: 12px;
            border-bottom: 3px solid transparent;
        }
        .sidebar-tab.active {
            border-bottom-color: var(--vscode-button-background);
            background: var(--vscode-sideBar-background, #252526);
        }
        .sidebar-content {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }
        .file-tree {
            display: none;
        }
        .file-tree.active {
            display: block;
        }
        .file-item {
            padding: 4px 8px;
            cursor: pointer;
            user-select: none;
            border-radius: 2px;
            font-size: 13px;
        }
        .file-item:hover {
            background: var(--vscode-list-hoverBackground);
        }
        .file-item.active {
            background: var(--vscode-list-activeSelectionBackground);
            color: var(--vscode-list-activeSelectionForeground);
        }
        .file-item.folder {
            font-weight: 600;
            color: var(--vscode-symbolIcon-folderForeground);
        }
        .file-indent { margin-left: 16px; }
        .file-indent-2 { margin-left: 32px; }
        
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .tabs {
            display: flex;
            background: var(--vscode-tab-inactiveBackground);
            border-bottom: 1px solid var(--vscode-panel-border);
        }
        .tab-button {
            padding: 10px 16px;
            background: transparent;
            color: var(--vscode-tab-inactiveForeground);
            border: none;
            cursor: pointer;
            font-size: 13px;
            border-bottom: 3px solid transparent;
            white-space: nowrap;
        }
        .tab-button.active {
            color: var(--vscode-tab-activeForeground);
            border-bottom-color: var(--vscode-button-background);
            background: var(--vscode-tab-activeBackground);
        }
        .tab-content {
            flex: 1;
            display: none;
            flex-direction: column;
            overflow: hidden;
        }
        .tab-content.active {
            display: flex;
        }
        
        .editor-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .editor-filename {
            padding: 8px 12px;
            background: var(--vscode-editor-background);
            border-bottom: 1px solid var(--vscode-panel-border);
            font-size: 12px;
            color: var(--vscode-descriptionForeground);
        }
        .editor-content {
            flex: 1;
            overflow: auto;
            padding: 0;
            background: var(--vscode-editor-background);
        }
        .editor-content code {
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.5;
        }
        .editor-content pre {
            margin: 0;
            padding: 12px;
            overflow: auto;
        }
        
        .terminal-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--vscode-editor-background);
            border: 1px solid var(--vscode-panel-border);
            overflow: hidden;
        }
        .terminal-header {
            padding: 8px 12px;
            background: var(--vscode-panel-background);
            border-bottom: 1px solid var(--vscode-panel-border);
            font-size: 12px;
            font-weight: 600;
        }
        .terminal-output {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.5;
            color: var(--vscode-terminal-foreground);
        }
        .terminal-line {
            margin-bottom: 2px;
        }
        .terminal-error {
            color: var(--vscode-terminal-ansiRed);
        }
        .terminal-success {
            color: var(--vscode-terminal-ansiGreen);
        }
        
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .message {
            padding: 10px 12px;
            border-radius: 4px;
            word-wrap: break-word;
            white-space: pre-wrap;
        }
        .user-message {
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            margin-left: 40px;
        }
        .agent-message {
            background: var(--vscode-panel-background);
            color: var(--vscode-editor-foreground);
            margin-right: 40px;
            border-left: 3px solid var(--vscode-button-background);
        }
        
        .input-section {
            display: flex;
            gap: 8px;
            padding: 12px;
            background: var(--vscode-editor-background);
            border-top: 1px solid var(--vscode-panel-border);
        }
        input {
            flex: 1;
            padding: 8px;
            border: 1px solid var(--vscode-inputBox-border);
            background: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
            border-radius: 4px;
            font-family: inherit;
        }
        input:focus {
            outline: none;
            border: 1px solid var(--vscode-focusBorder);
        }
        button {
            padding: 8px 16px;
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-family: inherit;
            font-size: 12px;
        }
        button:hover:not(:disabled) {
            background: var(--vscode-button-hoverBackground);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .action-buttons {
            display: flex;
            gap: 8px;
            padding: 10px;
            background: var(--vscode-panel-background);
            border-bottom: 1px solid var(--vscode-panel-border);
            flex-wrap: wrap;
        }
        .action-buttons button {
            padding: 6px 12px;
            font-size: 11px;
        }
        
        .scroll-container::-webkit-scrollbar {
            width: 12px;
        }
        .scroll-container::-webkit-scrollbar-track {
            background: transparent;
        }
        .scroll-container::-webkit-scrollbar-thumb {
            background: var(--vscode-scrollbarSlider-background);
            border-radius: 4px;
        }
        .scroll-container::-webkit-scrollbar-thumb:hover {
            background: var(--vscode-scrollbarSlider-hoverBackground);
        }
    </style>
</head>
<body>
    <div class="main-container">
        <!-- Sidebar: Files & Commands -->
        <div class="sidebar scroll-container">
            <div class="sidebar-tabs">
                <button class="sidebar-tab active" onclick="switchSidebarTab('files')">📁 Files</button>
                <button class="sidebar-tab" onclick="switchSidebarTab('commands')">⚙️ Commands</button>
            </div>
            <div class="sidebar-content">
                <div id="filesPanel" class="file-tree active"></div>
                <div id="commandsPanel" class="file-tree">
                    <div style="padding: 10px;">
                        <div class="action-buttons" style="flex-direction: column; padding: 0;">
                            <button onclick="createNewFile()" style="width: 100%; justify-content: flex-start;">+ New File</button>
                            <button onclick="createNewFolder()" style="width: 100%; justify-content: flex-start;">+ New Folder</button>
                            <button onclick="showRunCommand()" style="width: 100%; justify-content: flex-start;">▶ Run Command</button>
                            <button onclick="buildProject()" style="width: 100%; justify-content: flex-start;">🔨 Build</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Main Content Area -->
        <div class="main-content scroll-container">
            <div class="tabs">
                <button class="tab-button active" onclick="switchTab('editor')">Code Editor</button>
                <button class="tab-button" onclick="switchTab('terminal')">Terminal</button>
                <button class="tab-button" onclick="switchTab('chat')">Chat</button>
            </div>
            
            <!-- Code Editor Tab -->
            <div id="editor" class="tab-content active">
                <div class="action-buttons">
                    <button onclick="saveFile()">💾 Save</button>
                    <button onclick="deleteFile()">🗑️ Delete</button>
                    <button onclick="runFile()">▶ Run File</button>
                </div>
                <div class="editor-filename" id="editorTitle">No file selected</div>
                <div class="editor-area">
                    <div class="editor-content" id="editorContent">
                        <pre><code>Select a file to view or create a new one</code></pre>
                    </div>
                </div>
            </div>
            
            <!-- Terminal Tab -->
            <div id="terminal" class="tab-content">
                <div class="terminal-area">
                    <div class="terminal-header">Terminal Output</div>
                    <div class="terminal-output scroll-container" id="terminalOutput"></div>
                </div>
                <div class="input-section">
                    <input type="text" id="cmdInput" placeholder="Enter command..." />
                    <button onclick="executeCommand()">Execute</button>
                </div>
            </div>
            
            <!-- Chat Tab -->
            <div id="chat" class="tab-content">
                <div class="messages scroll-container" id="messages">
                    <div class="agent-message">✓ DAN Coding Suite loaded. Make sure Flask app is running (python app.py)</div>
                </div>
                <div class="input-section">
                    <input type="text" id="input" placeholder="Ask me anything..." />
                    <button id="send" onclick="sendMessage()">Send</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        let allFiles = [];
        let isLoadingFiles = false;

        function switchSidebarTab(tab) {
            document.querySelectorAll('.sidebar-tab').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('[id$="Panel"]').forEach(p => p.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tab + 'Panel').classList.add('active');
            if (tab === 'files') loadFileList();
        }

        function switchTab(tab) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
            document.getElementById(tab).classList.add('active');
            event.target.classList.add('active');
        }

        async function loadFileList() {
            if (isLoadingFiles) return;
            isLoadingFiles = true;
            vscode.postMessage({ command: 'listFiles' });
        }

        function renderFileList(files) {
            const panel = document.getElementById('filesPanel');
            panel.innerHTML = '';
            
            function renderItems(items, indent = 0) {
                items.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'file-item' + (item.folder ? ' folder' : '');
                    if (indent > 0) div.classList.add('file-indent' + (indent > 1 ? '-2' : ''));
                    div.textContent = (item.folder ? '📁 ' : '📄 ') + item.name;
                    div.onclick = () => {
                        if (!item.folder) {
                            loadFile(item.path);
                        }
                    };
                    panel.appendChild(div);
                    if (item.folder && item.children) {
                        renderItems(item.children, indent + 1);
                    }
                });
            }
            renderItems(files);
            isLoadingFiles = false;
        }

        function loadFile(path) {
            vscode.postMessage({ command: 'readFile', path });
        }

        function saveFile() {
            if (!currentFile) {
                alert('No file selected');
                return;
            }
            vscode.postMessage({ 
                command: 'saveFile',
                path: currentFile,
                content: document.getElementById('editorContent').innerText
            });
        }

        function deleteFile() {
            if (!currentFile) {
                alert('No file selected');
                return;
            }
            if (confirm('Delete ' + currentFile + '?')) {
                vscode.postMessage({ command: 'deleteFile', path: currentFile });
            }
        }

        function runFile() {
            if (!currentFile) {
                alert('No file selected');
                return;
            }
            vscode.postMessage({ command: 'runFile', path: currentFile });
        }

        function createNewFile() {
            const name = prompt('New file name:', 'file.txt');
            if (name) vscode.postMessage({ command: 'createFile', name });
        }

        function createNewFolder() {
            const name = prompt('New folder name:', 'folder');
            if (name) vscode.postMessage({ command: 'createFolder', name });
        }

        function showRunCommand() {
            document.getElementById('cmdInput').value = '';
            switchTab('terminal');
            document.getElementById('cmdInput').focus();
        }

        function executeCommand() {
            const cmd = document.getElementById('cmdInput').value.trim();
            if (!cmd) return;
            vscode.postMessage({ command: 'executeCmd', cmd });
            document.getElementById('cmdInput').value = '';
        }

        function buildProject() {
            vscode.postMessage({ command: 'buildProject' });
        }

        function addTerminalLine(text, type = 'normal') {
            const output = document.getElementById('terminalOutput');
            const line = document.createElement('div');
            line.className = 'terminal-line' + (type ? ' terminal-' + type : '');
            line.textContent = text;
            output.appendChild(line);
            output.scrollTop = output.scrollHeight;
        }

        function addChatMessage(text, isUser = false) {
            const messagesDiv = document.getElementById('messages');
            const msgDiv = document.createElement('div');
            msgDiv.className = isUser ? 'message user-message' : 'message agent-message';
            msgDiv.textContent = text;
            messagesDiv.appendChild(msgDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        async function sendMessage() {
            const input = document.getElementById('input').value.trim();
            if (!input) return;
            addChatMessage(input, true);
            document.getElementById('input').value = '';
            vscode.postMessage({ command: 'ask', text: input });
        }

        document.getElementById('input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        document.getElementById('cmdInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') executeCommand();
        });

        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.command) {
                case 'fileList':
                    renderFileList(message.files);
                    break;
                case 'fileContent':
                    document.getElementById('editorTitle').textContent = '📄 ' + message.path;
                    const pre = document.createElement('pre');
                    const code = document.createElement('code');
                    code.className = 'language-' + (message.extension || 'text');
                    code.textContent = message.content;
                    pre.appendChild(code);
                    document.getElementById('editorContent').innerHTML = '';
                    document.getElementById('editorContent').appendChild(pre);
                    hljs.highlightElement(code);
                    currentFile = message.path;
                    break;
                case 'terminalOutput':
                    addTerminalLine(message.text, message.type);
                    break;
                case 'chatResponse':
                    addChatMessage(message.response);
                    break;
                case 'error':
                    addTerminalLine('ERROR: ' + message.text, 'error');
                    break;
            }
        });

        loadFileList();
    </script>
</body>
</html>`;
}

function activate(context) {
    console.log('DAN AI Coding Suite extension activated');

    context.subscriptions.push(
        vscode.commands.registerCommand('danAi.openPanel', () => {
            if (currentPanel) {
                currentPanel.reveal(vscode.ViewColumn.Two);
                return;
            }

            currentPanel = vscode.window.createWebviewPanel(
                'danAi',
                'DAN AI Coding Suite',
                vscode.ViewColumn.Two,
                { 
                    enableScripts: true,
                    retainContextWhenHidden: true
                }
            );

            currentPanel.webview.html = getWebviewContent();

            currentPanel.webview.onDidReceiveMessage(async (message) => {
                const sendMessage = (cmd, data = {}) => {
                    currentPanel.webview.postMessage({ command: cmd, ...data });
                };

                try {
                    switch (message.command) {
                        case 'listFiles':
                            const filesData = await apiCall('/project_files');
                            sendMessage('fileList', { files: filesData.files || [] });
                            break;

                        case 'readFile':
                            const fileData = await apiCall('/read_file', 'POST', { path: message.path });
                            if (fileData.error) {
                                sendMessage('error', { text: fileData.error });
                            } else {
                                const ext = message.path.split('.').pop();
                                sendMessage('fileContent', { 
                                    path: message.path,
                                    content: fileData.content,
                                    extension: ext
                                });
                            }
                            break;

                        case 'saveFile':
                            const saveData = await apiCall('/write_file', 'POST', { 
                                path: message.path, 
                                content: message.content 
                            });
                            sendMessage('terminalOutput', { 
                                text: saveData.error ? '❌ Save failed: ' + saveData.error : '✓ File saved: ' + message.path,
                                type: saveData.error ? 'error' : 'success'
                            });
                            break;

                        case 'deleteFile':
                            const delData = await apiCall('/delete_file', 'POST', { path: message.path });
                            sendMessage('terminalOutput', { 
                                text: delData.error ? '❌ Delete failed: ' + delData.error : '✓ Deleted: ' + message.path,
                                type: delData.error ? 'error' : 'success'
                            });
                            break;

                        case 'runFile':
                            sendMessage('terminalOutput', { text: '▶ Running: ' + message.path, type: 'normal' });
                            const runData = await apiCall('/run_file', 'POST', { path: message.path });
                            if (runData.output) {
                                runData.output.split('\n').forEach(line => {
                                    if (line) sendMessage('terminalOutput', { text: line, type: 'normal' });
                                });
                            }
                            if (runData.error) {
                                sendMessage('terminalOutput', { text: runData.error, type: 'error' });
                            }
                            break;

                        case 'createFile':
                            const createData = await apiCall('/create_file', 'POST', { name: message.name });
                            sendMessage('terminalOutput', { 
                                text: createData.error ? '❌ ' + createData.error : '✓ Created: ' + message.name,
                                type: createData.error ? 'error' : 'success'
                            });
                            setTimeout(() => apiCall('/project_files').then(f => 
                                sendMessage('fileList', { files: f.files || [] })
                            ), 500);
                            break;

                        case 'executeCmd':
                            sendMessage('terminalOutput', { text: '$ ' + message.cmd, type: 'normal' });
                            const cmdData = await apiCall('/execute_cmd', 'POST', { cmd: message.cmd });
                            if (cmdData.output) {
                                cmdData.output.split('\n').forEach(line => {
                                    if (line) sendMessage('terminalOutput', { text: line, type: 'normal' });
                                });
                            }
                            if (cmdData.error) {
                                sendMessage('terminalOutput', { text: cmdData.error, type: 'error' });
                            }
                            break;

                        case 'buildProject':
                            sendMessage('terminalOutput', { text: '🔨 Building project...', type: 'normal' });
                            const buildData = await apiCall('/build', 'POST', {});
                            if (buildData.output) {
                                buildData.output.split('\n').forEach(line => {
                                    if (line) sendMessage('terminalOutput', { text: line, type: 'normal' });
                                });
                            }
                            if (buildData.error) {
                                sendMessage('terminalOutput', { text: buildData.error, type: 'error' });
                            }
                            break;

                        case 'ask':
                            const aiData = await apiCall('/think', 'POST', { input: message.text });
                            sendMessage('chatResponse', { response: aiData.response || aiData.error || 'No response' });
                            break;
                    }
                } catch (error) {
                    sendMessage('error', { text: error.message });
                }
            });

            currentPanel.onDidDispose(() => {
                currentPanel = null;
            });
        })
    );

    const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBar.command = 'danAi.openPanel';
    statusBar.text = '$(sparkle) DAN Code';
    statusBar.tooltip = 'Open DAN AI Coding Suite';
    statusBar.show();
    context.subscriptions.push(statusBar);
}

function deactivate() {}

module.exports = { activate, deactivate };
