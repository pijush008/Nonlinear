# app.py - CORRECTED version
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Auto-detect template folder
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

if os.path.exists(template_dir):
    app.template_folder = template_dir
else:
    # Fallback to default 'templates' folder
    app.template_folder = None

if os.path.exists(static_dir):
    app.static_folder = static_dir
else:
    app.static_folder = None

# Import solvers after app configuration
try:
    from picard import solve_picard
    from newton import solve_newton
    from euler import solve_euler
except ImportError as e:
    print(f"Import error: {e}")
    # Define fallback functions if modules can't be imported
    def solve_picard(*args, **kwargs):
        return {'error': 'Picard solver not available'}
    
    def solve_newton(*args, **kwargs):
        return {'error': 'Newton solver not available'}
    
    def solve_euler(*args, **kwargs):
        return {'error': 'Euler solver not available'}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received'})
        
        fx_str = data.get('equation', '').strip()
        x0 = data.get('x0')
        method = data.get('method', '').lower()
        
        if not fx_str:
            return jsonify({'error': 'Equation is required'})
        
        if x0 is None:
            return jsonify({'error': 'Initial guess (x0) is required'})
        
        try:
            x0 = float(x0)
        except (TypeError, ValueError):
            return jsonify({'error': 'Initial guess must be a valid number'})
        
        valid_methods = ['picard', 'newton', 'euler']
        if method not in valid_methods:
            return jsonify({'error': f'Method must be one of: {", ".join(valid_methods)}'})

        # Solve using the selected method
        if method == 'picard':
            result = solve_picard(fx_str, x0)
        elif method == 'newton':
            result = solve_newton(fx_str, x0)
        elif method == 'euler':
            step_size = float(data.get('step_size', 0.1))
            steps = int(data.get('steps', 10))
            result = solve_euler(fx_str, x0, step_size, steps)
            
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in solve route: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'})

if __name__ == '__main__':
    # Create Templates folder if it doesn't exist
    if not os.path.exists('Templates'):
        os.makedirs('Templates')
        print("Created Templates folder")
    
    if not os.path.exists('static'):
        os.makedirs('static')
        print("Created static folder")
    
    app.run(debug=True, port=5000)