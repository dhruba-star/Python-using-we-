from flask import Flask, request, jsonify
from sympy import symbols, factor, expand, simplify, Eq
from sympy.parsing.sympy_parser import parse_expr
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend calls

x = symbols('x')  # You can add more symbols as needed

def get_factorization_steps(expr):
    steps = []
    
    # Step 1: Simplify expression
    simplified = simplify(expr)
    steps.append(f"Step 1: Simplify the expression: {simplified}")
    
    # Step 2: Factor the expression (if it can be factored)
    factored = factor(simplified)
    steps.append(f"Step 2: Factor the expression: {factored}")
    
    # Step 3: If it's a quadratic, explain the factorization process
    if expr.is_polynomial(x) and expr.degree(x) == 2:
        a, b, c = expr.as_coefficients_dict()[x**2], expr.as_coefficients_dict().get(x, 0), expr.as_coefficients_dict().get(1, 0)
        steps.append(f"Step 3: For quadratic ax^2 + bx + c, find factors of ac = {a * c} that add up to {b}.")
        
        factors = []
        for i in range(1, abs(a * c) + 1):
            if a * c % i == 0 and (a * c // i + b == 0):
                factors = [i, a * c // i]
                break
        steps.append(f"Step 4: The factors of {a * c} are {factors}. We can now factor the quadratic.")
    
    return steps

@app.route('/factor', methods=['POST'])
def factorize():
    data = request.get_json()
    expr = data.get('expression', '')

    try:
        parsed_expr = parse_expr(expr)
        
        # Get step-by-step factorization
        steps = get_factorization_steps(parsed_expr)
        
        return jsonify({
            'input': expr,
            'steps': steps
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/simplify', methods=['POST'])
def simplify_expression():
    data = request.get_json()
    expr = data.get('expression', '')

    try:
        parsed_expr = parse_expr(expr)
        simplified = simplify(parsed_expr)
        return jsonify({
            'input': expr,
            'simplified': str(simplified)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
