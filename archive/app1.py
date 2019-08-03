
from sklearn.externals.joblib import dump, load
import pandas as pd
import tensorflow as tf
from flask import Flask, request
import numpy as np
from flask import Flask, request, jsonify
import keras
from keras import backend as K
import tensorflow.compat.v1 as tf
from sklearn.externals.joblib import dump, load
from sklearn.preprocessing import StandardScaler,MinMaxScaler


app = Flask(__name__)
model = None
graph = None


app.config['UPLOAD_FOLDER'] = 'uploads'





def load_model():
    global model
    global graph
    model = tf.keras.models.load_model("movie_model_trained.h5")
    graph  = tf.get_default_graph()

load_model()



@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    dd = {"success": False}
    if request.method == 'POST':
        Budget = int(request.form["Budget"])
        Comment = int(request.form["Comment"])
        View = int(request.form["View"])
        like = int(request.form["like"])
        likep= like/View
        Commentp=Comment/View
        data=[]
        data.append(Budget)
        data.append(Comment)
        data.append(View)
        data.append(like)
        data.append(likep)
        data.append(Commentp)
        sc=load('std_scaler.bin')



        with graph.as_default():
            with tf.Session() as sess:
                sess.run(tf.global_variables_initializer())
                sess.run(tf.tables_initializer())
                a=[]
                a = model.predict_classes(sc.transform(np.array(data).reshape(-1,1).T))
                print(a)
               

            dd["prediction"] = str(a[0])
            dd["success"] = True
            data=[]
            return jsonify(dd)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method="POST">
     <input type="number" name="Budget">
     <input type="number" name="Comment">
     <input type="number" name="View">
     <input type="number" name="like">


    <input type="submit">
    <input type="reset" value="REFRESH">

</form>
    '''


if __name__ == "__main__":
    app.run(debug=True)
