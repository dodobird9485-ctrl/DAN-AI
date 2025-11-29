import os
import sys

print("Script starting...")
sys.stdout.flush()

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
print(f"PROJECT_ROOT: {PROJECT_ROOT}")
sys.stdout.flush()

USER_FILES_DIR = os.path.join(PROJECT_ROOT, 'user_files')
print(f"USER_FILES_DIR: {USER_FILES_DIR}")
sys.stdout.flush()

def get_user_dir(user_id):
    user_dir = os.path.join(USER_FILES_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

test_user_id = 'user_test123'
user_dir = get_user_dir(test_user_id)

print(f"User directory: {user_dir}")
print(f"Directory exists: {os.path.exists(user_dir)}")
print(f"Directory contents: {os.listdir(user_dir)}")
sys.stdout.flush()

# Create a test file
test_file = os.path.join(user_dir, 'test.txt')
with open(test_file, 'w') as f:
    f.write('Hello, World!')

print(f"Test file created: {test_file}")
print(f"Directory contents after: {os.listdir(user_dir)}")
sys.stdout.flush()
