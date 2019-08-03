from flask import (
    Flask, 
    jsonify,
    render_template)
import json
import pandas as pd 

app = Flask(__name__, template_folder="templates")

file = "Resources/Data/movies.csv"
df = pd.read_csv(file)

years = {
    2016 : 1,
    2017 : 2, 
    2018 : 3
}

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/released_year/<year>")
def released_year(year):
    selected_yr = df.loc[df["year"] == int(year)]
    year_df = json.loads(selected_yr.to_json(orient='records'))
    return jsonify(year_df)

@app.route("/select_year")
def select_year():
    return (jsonify(list(years)))

@app.route("/movies_api")
def movies_api():
    data = json.loads(df.to_json(orient='records'))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
