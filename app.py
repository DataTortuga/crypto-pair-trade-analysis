from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import pair_model

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
#mongo = PyMongo(app)

@app.route("/")
def index():
    #mars_nws = mongo.db.mars_nws.find_one()
    return render_template("index.html")

@app.route("/about")
def about():
    #mars_nws = mongo.db.mars_nws.find_one()
    return render_template("about.html")


@app.route("/post")
def post():
    #mars_nws = mongo.db.mars_nws.find_one()
    return render_template("post.html")

@app.route("/pair/<window>")
def model(window):

    test_data = pair_model.model(int(window))
    
    return jsonify(test_data.tolist())


if __name__ == "__main__":
    app.run(debug=True)