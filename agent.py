from nearai.agents.environment import Environment

def check_for_todos_and_incomplete(code: str) -> list:
    findings = []
    
    # Check for TODO comments (including variations)
    todo_patterns = ['TODO', 'FIXME', 'XXX', 'HACK', 'BUG']
    for line_num, line in enumerate(code.split('\n'), 1):
        for pattern in todo_patterns:
            if pattern in line.upper():
                findings.append(f"Line {line_num}: Found {pattern} comment - {line.strip()}")
    
    # Check for potentially incomplete functions
    lines = code.split('\n')
    for i, line in enumerate(lines, 1):
        # Look for function definitions with pass or empty body
        if 'def ' in line and ':' in line:
            next_line_idx = i
            while next_line_idx < len(lines) and lines[next_line_idx].strip() == '':
                next_line_idx += 1
            if next_line_idx < len(lines):
                next_line = lines[next_line_idx].strip()
                if next_line == 'pass' or not next_line:
                    findings.append(f"Line {i}: Potentially incomplete function - {line.strip()}")
    
    return findings

def run(env: Environment):
    messages = env.list_messages()
    if not messages:
        # Initial prompt to request code to analyze
        env.add_reply("Please provide the code you'd like me to analyze for TODOs and incomplete functions.")
        env.request_user_input()
        return

    # Get the latest message (which should contain code)
    latest_message = messages[-1]['content']
    
    # Analyze the code
    findings = check_for_todos_and_incomplete(latest_message)
    
    if findings:
        response = "I found the following items that need attention:\n\n"
        response += "\n".join(findings)
    else:
        response = "No TODOs or incomplete functions found in the provided code."
    
    env.add_reply(response)
    env.request_user_input()

run(env)

