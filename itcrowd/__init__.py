from flask import Flask, render_template
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/itcrowddb"
mongo = PyMongo(app)

@app.route('/')
def home():
    test = mongo.db.test.insert_one({'test': 1234})
    t = mongo.db.test.find({'test:': 1234})
    print(t)
    return render_template('index.html')
