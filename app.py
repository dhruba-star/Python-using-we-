from flask import Flask, request, jsonify
from sympy import symbols, factor
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Add support for implicit multiplication and ^ as exponentiation
transformations = (standard_transformations + (implicit_multiplication_application, convert_xor))

# Define allowed symbols
x, y, z = symbols('x y z')

@app.route('/factor', methods=['POST'])
def factorize():
    data = request.get_json()
    expr = data.get('expression', '')

    try:
        parsed_expr = parse_expr(expr, transformations=transformations, evaluate=True)
        factored = factor(parsed_expr)
        return jsonify({
            'input': expr,
            'factored': str(factored)
        })
    except Exception as e:
        return jsonify({'error': f'Error while processing: {str(e)}'}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
