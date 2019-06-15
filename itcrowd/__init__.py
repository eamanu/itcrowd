from flask import (Flask, render_template)
from flask_pymongo import PyMongo
from flask_restful import Api
from bson.objectid import ObjectId
import json
import datetime


__all__ = ['app', 'db']

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/itcrowddb"
db = PyMongo(app).db
app.config['SECRET_KEY'] = 'dev'

"""
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime): 
            return str(o)
        return json.JSONEncoder.default(self, o)

app.json_encoder = JSONEncoder
"""
from itcrowd import routes
from itcrowd import models

# API
from itcrowd.api.v1 import (
        SayHello,
        GetAllPeople,
        GetPersonByAlias,
        GetPersonByFirstName,
        GetPersonByLastName,
        SetPerson,
        SetMovies,
        GetMoviesByTitle,
        AddPersonToMovieAs
    )

api = Api(app)
# Say Hello :-)
api.add_resource(SayHello, '/SayHello')
api.add_resource(GetAllPeople, '/GetAllPeople')
api.add_resource(GetPersonByAlias, '/GetPersonByAlias/<string:alias>')
api.add_resource(GetPersonByFirstName, '/GetPersonByFirstName/<string:first_name>')
api.add_resource(GetPersonByLastName, '/GetPersonByLastName/<string:last_name>')
api.add_resource(SetPerson, '/Person')
api.add_resource(SetMovies, '/Movies')
api.add_resource(GetMoviesByTitle, '/Movies/<string:title>')
api.add_resource(AddPersonToMovieAs, '/AddPersonToMovieAs')
