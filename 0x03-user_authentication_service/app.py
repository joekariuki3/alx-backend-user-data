#!/usr/bin/env python3
"""Flask app"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home() -> str:
    """home route/ default route
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
