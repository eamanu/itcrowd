from flask_restful import Resource, reqparse
from flask import request
from itcrowd.models import Person, Movies
from itcrowd import *
# from flask import jsonify
from bson.json_util import dumps


not_exist = {'message': 'does not exist'}
ok = {'message': 'Operation ok'}

parser = reqparse.RequestParser()


class SayHello(Resource):
    def get(self):
        return {'message': 'Hello World'}


class GetAllPeople(Resource):
    def get(self):
        return dumps(db.person.find({}))


class GetPersonByAlias(Resource):
    def get(self, alias: str):
        p = db.person.find({'aliases': alias})
        if p:
            return dumps(p)
        else:
            return not_exist, 400


class GetPersonByFirstName(Resource):
    def get(self, first_name: str):
        p = db.person.find({'first_name': first_name})
        if p:
            return dumps(p)
        else:
            return not_exist, 400


class GetPersonByLastName(Resource):
    def get(self, last_name: str):
        p = db.person.find({'last_name': last_name})
        if p:
            return dumps(p)
        else:
            return not_exist, 400


class SetPerson(Resource):
    def post(self):
        args = parser.parse_args()

        person = Person(args['first_name'], args['last_name'], args['alias'])
        if not person.save():
            return ok, 201
        else:
            return 400


class SetMovies(Resource):
    def post(self):
        args = request.get_json(force=True)
        movies = Movies(args['title'], args['year']) 
        if not movies.save():
            return ok, 201
        else:
            return {"message": "movies is already on database"}, 400


class GetMoviesByTitle(Resource):
    def get(self, title: str):
        m = db.movies.find({'title': title})
        if m:
            return dumps(m)
        else:
            return not_exist, 400

class AddPersonToMovieAs(Resource):
    def put(self):
        director, productor, actor = False
        args = parser.parse_args()
        person = db.person.find({'alias': args['alias']})
        movies = db.movies.find({'title': args['title']})
        p, m = None
        if args['like'] == 'director':
            p = Person(person['last_name'], person['first_name'], person['alias'],
                       movies_as_director=[movies['_id']])
            p.save_movies()
            m = Movies(movies['title'], movies['year'], directors=[person['_id']])
            m.save_people()
        elif args['like'] == 'productor':
            p = Person(person['last_name'], person['first_name'], person['alias'],
                       movies_as_productor=[movies['_id']])
            p.save_movies()
            m = Movies(movies['title'], movies['year'], productors=[person['_id']])
            m.save_people()
        elif args['like'] == 'actor':
            p = Person(person['last_name'], person['first_name'], person['alias'],
                       movies_as_actor=[movies['_id']])
            p.save_movies()
            m = Movies(movies['title'], movies['year'], casting=[person['_id']])
            m.save_people()
        else:
            return {'message': 'people like what?'} , 400

        return ok, 201

        
