from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import pair_model

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post")
def post():
    return render_template("post.html")

@app.route("/pair/<window>")
def model(window):

    test_data = pair_model.model(int(window))
    
    return jsonify(test_data.tolist())


if __name__ == "__main__":
    app.run(debug=True)