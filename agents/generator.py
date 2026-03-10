import requests
import re
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_code(prompt, output_dir=None):
    """
    Generates Code (Python or HTML) based on a prompt.
    Detects if the user wants a web page or a logic script.
    """
    prompt_lower = prompt.lower()
    
    # Intelligent Format Detection
    is_web = any(word in prompt_lower for word in ["web", "html", "css", "website", "page", "portfolio", "landing"])
    
    # Filename Logic
    words = re.findall(r'\w+', prompt_lower)
    name = words[0] if words else "feature"
    if is_web:
        filename = f"{name}.html"
    else:
        if "todo" in prompt_lower: name = "todo"
        elif "calculator" in prompt_lower: name = "calculator"
        filename = f"{name}_module.py"

    if is_web:
        system_prompt = """You are an expert Full-Stack Web Developer.
Output ONLY raw HTML code with internal CSS and JS. No markdown code blocks. No conversational text.
Create a visually stunning, premium-looking design. Use modern typography and gradients.
The entire app must be contained in a single .html file.
"""
    else:
        system_prompt = """You are an expert Python Software Engineer.
Output ONLY raw Python code. No markdown code blocks. No conversational text.

CRITICAL RULES:
1. THE CODE MUST BE 100% AUTOMATED (NO input() calls).
2. For calculators or managers: Call its methods 3-5 times in the main block to SHOW IT WORKS.
3. The entire script must run and finish in under 2 seconds.
"""

    # Try Gemini first
    if GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel('models/gemini-flash-latest')
            full_prompt = f"{system_prompt}\n\nUser Request: {prompt}"
            response = model.generate_content(full_prompt)
            
            code = response.text.strip()
            
            # Clean up markdown
            clean_code = code
            if "```html" in code: clean_code = code.split("```html")[1].split("```")[0].strip()
            elif "```python" in code: clean_code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code: clean_code = code.split("```")[1].split("```")[0].strip()
            
            code = clean_code.strip() + "\n"
            
            save_code(filename, code, output_dir)
            return {
                "status": "success",
                "code": code,
                "filename": filename,
                "model": "Gemini 1.5 Flash (Web/Python Enabled)"
            }
        except Exception as e:
            print(f"Gemini API Error: {str(e)}. Falling back to local model...")

    # Fallback to Local Llama 3.2
    try:
        response = requests.post("http://127.0.0.1:11434/api/generate", json={
            "model": "llama3.2:1b",
            "prompt": f"{system_prompt}\n\nUser Request: {prompt}",
            "stream": False
        }, timeout=15)
        
        response.raise_for_status()
        raw_output = response.json().get("response", "")
        
        code = raw_output
        if "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
            if code.startswith("html\n"): code = code[5:]
            if code.startswith("python\n"): code = code[7:]
            
        code = code.strip() + "\n"
        
        save_code(filename, code, output_dir)
        return {
            "status": "success",
            "code": code,
            "filename": filename,
            "model": "Llama 3.2 (Local)"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"All models failed. Last error: {str(e)}"
        }

def save_code(filename, code, output_dir=None):
    if not output_dir:
        output_dir = "generated_code"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, filename), "w", encoding='utf-8') as f:
        f.write(code)
