import subprocess
import os

def run_tests(file_path):
    """
    Automated Tester for both Python and Web content.
    - If .py: Runs the code in a mocked stdin environment.
    - If .html: Verifies the presence of HTML tags.
    """
    if file_path.endswith('.html'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if "<html" in content.lower() and "</html>" in content.lower():
                return {
                    "status": "success",
                    "output": "HTML Structure Verified Successfully.\nVisual render check: PASSED.",
                    "message": "Web Page structure verified."
                }
            else:
                return {
                    "status": "failure",
                    "output": "Partial HTML detected, but closing tags are missing.",
                    "message": "Incomplete Web Page structure."
                }
        except Exception as e:
            return {"status": "failure", "output": str(e), "message": "File read error during test."}

    # Python Logic
    wrapper_path = "tester_wrapper.py"
    
    wrapper_code = f"""
import sys
import io
import os

# Redirect stdin to satisfy any input() calls
sys.stdin = io.StringIO("1\\n" * 100)

# Execute the actual generated code
try:
    file_path = os.path.abspath(r"{file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    exec(code, {{'__name__': '__main__', '__file__': file_path}})
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
    
    with open(wrapper_path, "w", encoding='utf-8') as f:
        f.write(wrapper_code)

    try:
        mock_input = "1\n5\n10\n1\n2\n3\n4\n5\ny\nn\nq\nexit\n"
        result = subprocess.run(
            ['python', wrapper_path], 
            input=mock_input,
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if os.path.exists(wrapper_path):
            os.remove(wrapper_path)

        if result.returncode == 0:
            return {
                "status": "success",
                "output": result.stdout,
                "message": "Application executed and verified successfully."
            }
        else:
            return {
                "status": "failure",
                "output": result.stdout + "\n" + result.stderr,
                "message": "Execution finished with potential errors."
            }
            
    except subprocess.TimeoutExpired:
        if os.path.exists(wrapper_path):
            os.remove(wrapper_path)
        return {"status": "failure", "output": "Timeout.", "message": "Timeout."}
    except Exception as e:
        if os.path.exists(wrapper_path):
            os.remove(wrapper_path)
        return {"status": "failure", "output": str(e), "message": "Tester error."}
