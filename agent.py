from nearai.agents.environment import Environment
import os

def analyze_code_in_directory(directory: str) -> list:
    findings = []
    
    def analyze_file(filepath: str):
        with open(filepath, 'r') as f:
            code = f.read()
            
        # Check for TODO comments and variations
        todo_patterns = ['TODO', 'FIXME', 'XXX', 'HACK', 'BUG']
        for line_num, line in enumerate(code.split('\n'), 1):
            for pattern in todo_patterns:
                if pattern in line.upper():
                    findings.append(f"{filepath}:{line_num}: Found {pattern} comment - {line.strip()}")
        
        # Check for incomplete functions
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for incomplete function definitions
            if 'def ' in line and ':' in line:
                next_line_idx = i
                while next_line_idx < len(lines) and lines[next_line_idx].strip() == '':
                    next_line_idx += 1
                if next_line_idx < len(lines):
                    next_line = lines[next_line_idx].strip()
                    if next_line == 'pass' or not next_line:
                        findings.append(f"{filepath}:{i}: Potentially incomplete function - {line.strip()}")
            # Check for truncated code (like in your example)
            if line.strip().endswith('with open(wallet'):
                findings.append(f"{filepath}:{i}: Truncated code found - {line.strip()}")

    # Recursively walk through directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):  # Only analyze Python files
                filepath = os.path.join(root, file)
                try:
                    analyze_file(filepath)
                except Exception as e:
                    findings.append(f"Error analyzing {filepath}: {str(e)}")

    return findings

def run(env: Environment):
    # Get the workspace directory (assuming it's the current directory)
    workspace_dir = os.getcwd()
    
    # Analyze all Python files in the workspace
    findings = analyze_code_in_directory(workspace_dir)
    
    if findings:
        response = "I found the following items that need attention:\n\n"
        response += "\n".join(findings)
    else:
        response = "No TODOs or incomplete functions found in the codebase."
    
    env.add_reply(response)
    env.request_user_input()

run(env)


