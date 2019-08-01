from flask import Flask, render_template, url_for, request, jsonify
from flask_material import Material 
import simplejson as json
import pandas as pd 
import numpy as np 
from sklearn.externals import joblib



app = Flask(__name__, template_folder="templates")
Material(app)

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
    
    if request.method == 'POST':
        input_budget = request.form["budget"]
        input_comment = request.form["comment"]
        input_view = request.form["view"]
        input_like = request.form["like"]

        Budget = int(request.form["budget"])*1000000
        Comment = int(request.form["comment"])*1000000
        View = int(request.form["view"])*1000
        Like = int(request.form["like"])*1000
        Likep= Like/View
        Commentp=Comment/View
        # data=[]
        # data.append(Budget)
        # data.append(Comment)
        # data.append(View)
        # data.append(Like)
        # data.append(Likep)
        # data.append(Commentp)
        # sc=load('std_scaler.bin')

        # with graph.as_default():
        #     with tf.Session() as sess:
        #         sess.run(tf.global_variables_initializer())
        #         sess.run(tf.tables_initializer())
        #         a = model.predict_classes(sc.transform(np.array(data).reshape(-1,1).T))
        #         print(a)
        #     dd["prediction"] = str(a[0])
        #     dd["success"] = True

        #     return jsonify(dd)

    return render_template('index.html', input_budget=input_budget, input_comment=input_comment, input_view=input_view, input_like=input_like)


if __name__ == '__main__':
    app.run(debug=True)