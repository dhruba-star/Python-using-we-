from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import symbols, factor
from sympy.parsing.sympy_parser import parse_expr
import os
import re

app = Flask(__name__)
CORS(app)

# Define common symbols; add more as needed.
x, y, z = symbols('x y z')

def convert_superscript(expr_str):
    """
    Convert exponent patterns like '**2' into Unicode superscripts.
    For example, "x**2" becomes "x²".
    """
    # Define replacements for exponents.
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
        expr_str = expr_str.replace(k, v)
    return expr_str

@app.route('/factor', methods=['POST'])
def factorize():
    try:
        data = request.get_json()
        # Retrieve the expression and convert caret to double asterisk.
        raw_expr = data.get('expression', '').replace('^', '**')
        if not raw_expr:
            return jsonify({'error': 'No expression provided'}), 400

        # Parse and factor the expression.
        parsed_expr = parse_expr(raw_expr)
        factored = factor(parsed_expr)

        # Convert to a visually improved string.
        original_str = convert_superscript(str(parsed_expr))
        factored_str = convert_superscript(str(factored))

        # Prepare step-by-step explanation (basic).
        steps = []
        if parsed_expr == factored:
            steps.append("Expression cannot be factored further.")
        else:
            steps.append(f"Original: {original_str}")
            steps.append(f"Factored: {factored_str}")

        return jsonify({
            'input': original_str,
            'factored': factored_str,
            'steps': steps
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
