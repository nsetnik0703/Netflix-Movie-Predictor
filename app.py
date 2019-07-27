from flask import (
    Flask, 
    jsonify,
    render_template)
import json
import pandas as pd 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
