from flask import Flask, render_template, request, jsonify
from agent_advanced import AdvancedAgent
import json
import os
import subprocess
import glob
from pathlib import Path
import zipfile
import io
from flask import send_file

app = Flask(__name__)
agent = AdvancedAgent("policy.json")

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
USER_FILES_DIR = os.path.join(PROJECT_ROOT, 'user_files')
os.makedirs(USER_FILES_DIR, exist_ok=True)

def get_user_dir(user_id):
    user_dir = os.path.join(USER_FILES_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def is_safe_path(path, user_id=None):
    if user_id:
        user_dir = get_user_dir(user_id)
        full_path = os.path.normpath(os.path.join(user_dir, path))
        return full_path.startswith(user_dir)
    else:
        full_path = os.path.normpath(os.path.join(PROJECT_ROOT, path))
        return full_path.startswith(PROJECT_ROOT)

def get_project_structure(directory=PROJECT_ROOT, max_depth=3, current_depth=0):
    items = []
    if current_depth >= max_depth:
        return items
    
    ignore_dirs = {'.git', '__pycache__', 'node_modules', '.env', '.vscode', '.vscode-test'}
    
    try:
        for item in sorted(os.listdir(directory)):
            if item.startswith('.') and item not in {'.env', '.gitignore', '.vscodeignore'}:
                continue
            if item in ignore_dirs:
                continue
            
            path = os.path.join(directory, item)
            rel_path = os.path.relpath(path, PROJECT_ROOT)
            
            if os.path.isdir(path):
                items.append({
                    'name': item,
                    'path': rel_path,
                    'folder': True,
                    'children': get_project_structure(path, max_depth, current_depth + 1)
                })
            else:
                items.append({
                    'name': item,
                    'path': rel_path,
                    'folder': False
                })
    except Exception as e:
        pass
    
    return items

@app.route('/')
def index():
    return render_template('index.html', policy=agent.policy)

@app.route('/api/think', methods=['POST'])
def think():
    data = request.json
    user_input = data.get('input', '')
    user_id = data.get('userId', 'default')
    
    if not user_input:
        return jsonify({'error': 'Empty input'}), 400
    
    response = agent.respond(user_input, user_id=user_id)
    
    return jsonify({
        'response': response,
        'policy': agent.policy['name'],
        'memory_count': len(agent.memory),
        'log_count': len(agent.logs),
        'safe_mode': agent.policy.get('safe_mode', True)
    })

@app.route('/api/policy', methods=['GET'])
def get_policy():
    return jsonify(agent.policy)

@app.route('/api/policy', methods=['POST'])
def update_policy():
    data = request.json
    agent.policy.update(data)
    with open("policy.json", 'w') as f:
        json.dump(agent.policy, f, indent=2)
    return jsonify({'success': True, 'policy': agent.policy})

@app.route('/api/memory', methods=['GET'])
def get_memory():
    return jsonify(agent.memory)

@app.route('/api/logs', methods=['GET'])
def get_logs():
    return jsonify(agent.logs[-10:])

@app.route('/api/reload', methods=['POST'])
def reload_policy():
    agent.load_policy()
    return jsonify({'success': True, 'policy': agent.policy['name']})

@app.route('/api/toggle_safe_mode', methods=['POST'])
def toggle_safe_mode():
    agent.policy['safe_mode'] = not agent.policy.get('safe_mode', True)
    with open("policy.json", 'w') as f:
        json.dump(agent.policy, f, indent=2)
    mode = "SAFE (trusted sites)" if agent.policy['safe_mode'] else "UNRESTRICTED (full web)"
    return jsonify({'success': True, 'safe_mode': agent.policy['safe_mode'], 'mode': mode})

@app.route('/api/clear_memory', methods=['POST'])
def clear_memory():
    agent.memory = {}
    agent.save_memory()
    return jsonify({'success': True, 'message': 'Memory cleared'})

@app.route('/api/scrape', methods=['POST'])
def scrape():
    data = request.json
    url = data.get('url', '')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    content = agent.scrape_website(url)
    return jsonify({'content': content, 'url': url})

@app.route('/api/generated_files', methods=['GET'])
def generated_files():
    files = glob.glob('generated_*.*')
    result = {}
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                result[f] = file.read()
        except:
            result[f] = "Could not read file"
    return jsonify(result)

@app.route('/api/project_files', methods=['GET'])
def project_files():
    structure = get_project_structure()
    return jsonify({'files': structure})

@app.route('/api/user_files', methods=['GET'])
def user_files():
    user_id = request.args.get('user', 'default')
    user_dir = get_user_dir(user_id)
    print(f"DEBUG: user_files called with user_id={user_id}, user_dir={user_dir}")
    print(f"DEBUG: user_dir exists: {os.path.exists(user_dir)}")
    
    def get_user_structure(directory, max_depth=3, current_depth=0):
        items = []
        if current_depth >= max_depth:
            return items
        
        try:
            contents = os.listdir(directory)
            print(f"DEBUG: Listed {len(contents)} items in {directory}")
            for item in sorted(contents):
                if item.startswith('.'):
                    continue
                
                path = os.path.join(directory, item)
                rel_path = os.path.relpath(path, user_dir)
                
                if os.path.isdir(path):
                    items.append({
                        'name': item,
                        'path': rel_path,
                        'folder': True,
                        'children': get_user_structure(path, max_depth, current_depth + 1)
                    })
                else:
                    items.append({
                        'name': item,
                        'path': rel_path,
                        'folder': False
                    })
        except Exception as e:
            print(f"DEBUG: Exception in get_user_structure: {e}")
        
        return items
    
    structure = get_user_structure(user_dir)
    print(f"DEBUG: Returning {len(structure)} items")
    return jsonify({'files': structure})

@app.route('/api/read_file', methods=['POST'])
def read_file():
    data = request.json
    path = data.get('path', '')
    user_id = data.get('userId', 'default')
    
    if not is_safe_path(path, user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    user_dir = get_user_dir(user_id)
    full_path = os.path.join(user_dir, path)
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': f'Cannot read file: {str(e)}'}), 400

@app.route('/api/write_file', methods=['POST'])
def write_file():
    data = request.json
    path = data.get('path', '')
    content = data.get('content', '')
    user_id = data.get('userId', 'default')
    
    if not is_safe_path(path, user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    user_dir = get_user_dir(user_id)
    full_path = os.path.join(user_dir, path)
    
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'success': True, 'path': path})
    except Exception as e:
        return jsonify({'error': f'Cannot write file: {str(e)}'}), 400

@app.route('/api/delete_file', methods=['POST'])
def delete_file():
    data = request.json
    path = data.get('path', '')
    user_id = data.get('userId', 'default')
    
    if not is_safe_path(path, user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    user_dir = get_user_dir(user_id)
    full_path = os.path.join(user_dir, path)
    
    try:
        if os.path.isfile(full_path):
            os.remove(full_path)
            return jsonify({'success': True, 'path': path})
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Cannot delete file: {str(e)}'}), 400

@app.route('/api/create_file', methods=['POST'])
def create_file():
    data = request.json
    name = data.get('name', 'untitled.txt')
    user_id = data.get('userId', 'default')
    
    safe_name = os.path.basename(name)
    user_dir = get_user_dir(user_id)
    full_path = os.path.join(user_dir, safe_name)
    
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write('')
        return jsonify({'success': True, 'path': safe_name})
    except Exception as e:
        return jsonify({'error': f'Cannot create file: {str(e)}'}), 400

@app.route('/api/create_folder', methods=['POST'])
def create_folder():
    data = request.json
    name = data.get('name', 'newfolder')
    user_id = data.get('userId', 'default')
    
    safe_name = os.path.basename(name)
    user_dir = get_user_dir(user_id)
    full_path = os.path.join(user_dir, safe_name)
    
    if not is_safe_path(safe_name, user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        os.makedirs(full_path, exist_ok=True)
        return jsonify({'success': True, 'path': safe_name})
    except Exception as e:
        return jsonify({'error': f'Cannot create folder: {str(e)}'}), 400

@app.route('/api/run_file', methods=['POST'])
def run_file():
    data = request.json
    path = data.get('path', '')
    user_id = data.get('userId', 'default')
    
    if not is_safe_path(path, user_id):
        return jsonify({'error': 'Access denied'}), 403
    
    user_dir = get_user_dir(user_id)
    full_path = os.path.join(user_dir, path)
    
    try:
        ext = Path(path).suffix.lower()
        
        if ext == '.py':
            result = subprocess.run(['python', full_path], capture_output=True, text=True, timeout=10)
        elif ext == '.js':
            result = subprocess.run(['node', full_path], capture_output=True, text=True, timeout=10)
        elif ext == '.html':
            return jsonify({'error': 'HTML files need a browser to run. Open the file to view.'}), 400
        else:
            return jsonify({'error': f'Unsupported file type: {ext}'}), 400
        
        output = result.stdout if result.returncode == 0 else result.stderr
        return jsonify({'output': output, 'returncode': result.returncode})
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Program execution timed out'}), 408
    except Exception as e:
        return jsonify({'error': f'Cannot run file: {str(e)}'}), 400

@app.route('/api/execute_cmd', methods=['POST'])
def execute_cmd():
    data = request.json
    cmd = data.get('cmd', '')
    
    if not cmd:
        return jsonify({'error': 'No command provided'}), 400
    
    dangerous_cmds = ['rm -rf', 'del /s', 'format', 'mkfs', 'dd if=']
    if any(d in cmd.lower() for d in dangerous_cmds):
        return jsonify({'error': 'Command denied for safety'}), 403
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10, cwd=PROJECT_ROOT)
        output = result.stdout if result.returncode == 0 else result.stderr
        return jsonify({'output': output, 'returncode': result.returncode})
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command execution timed out'}), 408
    except Exception as e:
        return jsonify({'error': f'Cannot execute command: {str(e)}'}), 400

@app.route('/api/build', methods=['POST'])
def build():
    try:
        result = subprocess.run('python app.py', shell=True, capture_output=True, text=True, timeout=5, cwd=PROJECT_ROOT)
        output = result.stdout if result.returncode == 0 else result.stderr
        return jsonify({'output': output, 'returncode': result.returncode})
    except subprocess.TimeoutExpired:
        return jsonify({'output': 'Build started (check terminal)', 'returncode': 0})
    except Exception as e:
        return jsonify({'error': f'Build failed: {str(e)}'}), 400

@app.route('/api/export_project', methods=['POST'])
def export_project():
    data = request.json
    user_id = data.get('userId', 'default')
    user_dir = get_user_dir(user_id)
    
    try:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(user_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, user_dir)
                    zip_file.write(file_path, arcname=arcname)
        
        zip_buffer.seek(0)
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'project_{user_id}.zip'
        )
    except Exception as e:
        return jsonify({'error': f'Export failed: {str(e)}'}), 400

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🤖 AI AGENT - Advanced Web Interface")
    print("="*60)
    print("\nStarting server...")
    print("Open your browser to: http://localhost:5000")
    print("\nFeatures:")
    print("  • Web Search (Safe/Unrestricted modes)")
    print("  • Persistent Memory Storage")
    print("  • Real Tool Implementations")
    print("  • Command System (/help for commands)")
    print("  • File Operations (read/write/delete)")
    print("  • Code Execution (Python/Node.js)")
    print("  • Terminal Integration")
    print("\nPress CTRL+C to stop\n")
    app.run(debug=True, use_reloader=False)
