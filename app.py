import os
from flask import Flask, request, jsonify, render_template, send_from_directory

from agents.generator import generate_code
from agents.tester import run_tests
from agents.deployer import deploy_code

app = Flask(__name__)
GENERATED_DIR = os.path.join(os.path.dirname(__file__), 'generated_code')
os.makedirs(GENERATED_DIR, exist_ok=True)

# Temporary storage for latest results
latest_results = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view_result/<filename>')
def view_result(filename):
    # Live Web Preview Logic
    if filename.endswith('.html'):
        return send_from_directory(GENERATED_DIR, filename)
    
    # Python Terminal Logic
    output = latest_results.get(filename, "No result data available for this execution.")
    return render_template('result_view.html', filename=filename, output=output)

@app.route('/api/process', methods=['POST'])
def process_request():
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'No feature request provided'}), 400

    results = {}
    
    # Step 1: Generate Code
    try:
        gen_result = generate_code(prompt, GENERATED_DIR)
        results['generation'] = gen_result
        if gen_result['status'] != 'success':
            return jsonify({'step': 'generation', 'results': results, 'error': 'Code generation failed'}), 500
    except Exception as e:
        return jsonify({'step': 'generation', 'results': results, 'error': str(e)}), 500

    # Step 2: Test Code
    try:
        filename = gen_result['filename']
        file_path = os.path.join(GENERATED_DIR, filename)
        
        test_result = run_tests(file_path)
        results['testing'] = test_result
        
        # Store for terminal viewer (only relevant for .py)
        if not filename.endswith('.html'):
            latest_results[filename] = test_result.get('output', 'Execution complete.')
        
        if test_result['status'] != 'success':
            return jsonify({'step': 'testing', 'results': results, 'message': test_result.get('message', 'Tests failed')}), 400
    except Exception as e:
        return jsonify({'step': 'testing', 'results': results, 'error': str(e)}), 500

    # Step 3: Deploy Code
    try:
        deploy_result = deploy_code(file_path)
        results['deployment'] = deploy_result
        if deploy_result['status'] != 'success':
            return jsonify({'step': 'deployment', 'results': results, 'message': 'Deployment failed'}), 500
    except Exception as e:
         return jsonify({'step': 'deployment', 'results': results, 'error': str(e)}), 500

    return jsonify({'step': 'complete', 'results': results, 'message': 'Pipeline completed successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)
