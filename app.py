"""syzygy web application"""

from flask import Flask, jsonify
import syzygy

app = Flask(__name__)


@app.route('/')
def hello():
    """Return a simple string for the root webpage

    Will be replaced with frontend later on"""
    return 'Hello, World!'


# TODO use POST request and user-submitted C code
# @app.route('/view', methods=['POST'])
@app.route('/view', methods=['GET', 'POST'])
def struct_info():
    """Return JSON object describing structs in provided code"""
    # TODO get code as argument
    res = []
    structs = syzygy.parse_structs_from_file("test_struct.c")

    for entry in structs:
        res.append(entry.to_json())

    return jsonify(res)
