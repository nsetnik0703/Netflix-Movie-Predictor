from flask import (
    Flask, 
    jsonify,
    render_template)
import json
import pandas as pd 

app = Flask(__name__, template_folder="templates")

file = "Resources/Data/combined data/combined_2018.csv"
df_2018 = pd.read_csv(file)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/movies_api")
def movies_api():
    data = json.loads(df_2018.to_json(orient='records'))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
