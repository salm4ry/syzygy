"""syzygy web application"""

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import syzygy
import defaults
import env

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    """Return a simple string for the root webpage

    Will be replaced with frontend later on"""
    return 'Hello, World!'


@app.route('/view', methods=['POST'])
@cross_origin()
def struct_info():
    """Return JSON object describing structs in provided code"""
    res = []

    # get code from request body
    code_str = request.json.get("code")

    # split on newline
    structs = syzygy.parse_structs(code_str.split("\n"))

    for entry in structs:
        res.append(entry.to_json())

    return jsonify(res)


if __name__ == "__main__":
    # get port number (integer), and whether to enable debug mode (boolean)
    # from environment variables
    port = env.get_int("PORT", defaults.PORT)
    debug = env.get_bool("DEBUG", defaults.DEBUG)
    app.run(debug=debug, port=port)
