from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import symbols, factor, expand
from sympy.parsing.sympy_parser import parse_expr

app = Flask(__name__)
CORS(app)

x, y, a, b, c = symbols('x y a b c')  # Add more as needed

def convert_superscript(expr):
    # Replace exponents like **2 with proper Unicode superscript
    replacements = {
        '**2': '²',
        '**3': '³',
        '**4': '⁴',
        '**5': '⁵',
        '**6': '⁶',
        '**7': '⁷',
        '**8': '⁸',
        '**9': '⁹'
    }
    for k, v in replacements.items():
        expr = expr.replace(k, v)
    return expr

@app.route('/factor', methods=['POST'])
def factorize():
    try:
        data = request.get_json()
        raw_expr = data.get('expression', '').replace('^', '**')  # handle input like x^2
        parsed_expr = parse_expr(raw_expr)

        # Basic factorization
        factored = factor(parsed_expr)

        # For quadratic expressions, try to give a simple step explanation
        steps = []

        if parsed_expr == factored:
            steps.append("Expression cannot be factored further.")
        else:
            steps.append(f"Original: {convert_superscript(str(parsed_expr))}")
            steps.append(f"Factored: {convert_superscript(str(factored))}")

        return jsonify({'steps': steps})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
