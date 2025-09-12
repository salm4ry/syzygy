"""syzygy web application"""

from os import environ
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import syzygy

DEFAULT_PORT = 8000
DEFAULT_DEBUG = True

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    """Return a simple string for the root webpage

    Will be replaced with frontend later on"""
    return 'Hello, World!'


# TODO use POST request and user-submitted C code
# @app.route('/view', methods=['POST'])
@app.route('/view', methods=['GET', 'POST'])
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
    port = int(environ.get("PORT", DEFAULT_PORT))
    debug = environ.get("DEBUG", DEFAULT_DEBUG).lower() \
        in ("yes", "y", "true", "1", "t")
    app.run(debug=debug, port=port)
