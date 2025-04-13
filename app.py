from flask import Flask, request, jsonify
from sympy import symbols, factor
from sympy.parsing.sympy_parser import parse_expr
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend calls

x = symbols('x')  # You can add more symbols as needed

@app.route('/factor', methods=['POST'])
def factorize():
    data = request.get_json()
    expr = data.get('expression', '')

    try:
        parsed_expr = parse_expr(expr)
        factored = factor(parsed_expr)
        return jsonify({
            'input': expr,
            'factored': str(factored)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    import os

port = int(os.environ.get("PORT", 10000))
app.run(host='0.0.0.0', port=port)
