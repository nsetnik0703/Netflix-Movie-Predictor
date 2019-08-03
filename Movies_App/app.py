from flask import Flask, render_template, url_for, request, jsonify
from flask_material import Material 
import simplejson as json
import pandas as pd 
import numpy as np 
from sklearn.externals.joblib import dump, load
import keras
from keras import backend as K
import tensorflow as tf
from sklearn.preprocessing import StandardScaler,MinMaxScaler



app = Flask(__name__, template_folder="templates")
Material(app)

model = None
graph = None

def load_model():
    global model
    global graph
    model = tf.keras.models.load_model("Data/movie_model_trained.h5")
    graph  = tf.get_default_graph()

load_model()

file = "Data/movies.csv"
df = pd.read_csv(file)

years = {
    2016 : 1,
    2017 : 2, 
    2018 : 3
}

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/movies_api")
def movies_api():
    data = json.loads(df.to_json(orient='records'))
    return jsonify(data)

@app.route("/released_year/<year>")
def released_year(year):
    selected_yr = df.loc[df["year"] == int(year)]
    year_df = json.loads(selected_yr.to_json(orient='records'))
    return jsonify(year_df)

@app.route("/select_year")
def select_year():
    return (jsonify(list(years)))

@app.route('/analyze', methods=['POST','GET'])
def analyze():
    dd = {"success": False}

    if request.method == 'POST':
        input_budget = int(request.form["budget"])
        input_comment = int(request.form["comment"])
        input_view = float(request.form["view"])
        input_like = int(request.form["like"])
        input_likep=input_like/input_view
        input_commentp=input_comment/input_view

        data=[]
        data.append(input_budget*1000000)
        data.append(input_comment*1000000)
        data.append(input_view*1000)
        data.append(input_like*1000)
        data.append(input_likep)
        data.append(input_commentp)
        sc=load('Data/std_scaler.bin')

        with graph.as_default():
            with tf.Session() as sess:
                sess.run(tf.global_variables_initializer())
                sess.run(tf.tables_initializer())
                a = model.predict_classes(sc.transform(np.array(data).reshape(-1,1).T))
                print(a)
            dd["prediction"] = str(a[0])
            predict=str(a[0])
            dd["success"] = True

    return render_template('index.html', input_budget=input_budget, input_comment=input_comment, input_view=input_view, input_like=input_like, predict=predict)


if __name__ == '__main__':
    app.run(debug=True)