from flask_restful import Resource, reqparse
from flask import request
from itcrowd.models import Person, Movies
from itcrowd import *
# from flask import jsonify
from bson.json_util import dumps
from flask_httpauth import HTTPBasicAuth


not_exist = {'message': 'does not exist'}
ok = {'message': 'Operation ok'}

parser = reqparse.RequestParser()

auth = HTTPBasicAuth()

list_of_roman = [('I', 1), ('IV', 4), ('V', 5), ('IX', 9), ('X', 10),
                 ('XL', 40), ('L', 50), ('XC', 90), ('C' , 100),
                 ('CD', 400), ('D', 500), ('CM',900), ('M', 1000)]

list_of_roman = list(reversed(list_of_roman))

def to_roman(number: int, roman: str = '') -> str:
    for r, i in list_of_roman:
        if number >= i:
            return to_roman(number - i, roman + '%s' % (r))
    return roman


@auth.verify_password
def varify_password(username, password):
    if db.authentication.find_one({'user': username, 'password': password}):
        print("hola")
        return True
    return False


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
    decorators = [auth.login_required]
    def post(self):
        args = request.get_json(force=True)
        person = Person(args['first_name'], args['last_name'], args['alias'])
        if not person.save():
            return ok, 201
        else:
            return {"message": "This Person is already on database"}, 400


class SetMovies(Resource):
    decorators = [auth.login_required]
    def post(self):
        args = request.get_json(force=True)
        movies = Movies(args['title'], args['year']) 
        if not movies.save():
            return ok, 201
        else:
            return {"message": "movies is already on database"}, 400


class MoviesList(Resource):
    def get(self):
        m = list(db.movies.find({}))

        for d in m:
            d.update(("year", to_roman(value)) for k, value in d.items() if k == "year")
        return dumps(m)


class GetMoviesByTitle(Resource):
    def get(self, title: str):
        m = list(db.movies.find({'title': title}))
        if m:
            for d in dumps(m):
                d.update(("year", to_roman(value)) for k, value in d.items() if k == "year")
            return dumps(m)
        else:
            return not_exist, 400


class AddPersonToMovieAs(Resource):
    decorators = [auth.login_required]
    def put(self):
        args = request.get_json(force=True)
        person = db.person.find({'aliases': args['alias']})
        movies = db.movies.find({'title': args['title']})
        if not person.count() or not movies.count():
            return {"message": "Person or Movie does not exist"}, 400
        person = person[0]
        movies = movies[0]

        p = None
        m = None
        if args['like'] == 'director':
            p = Person(person['first_name'], person['last_name'], person['aliases'],
                       movies_as_director=[movies['_id']])
            p.save_movies()
            m = Movies(movies['title'], movies['year'], directors=[person['_id']])
            m.save_people()
        elif args['like'] == 'productor':
            p = Person(person['first_name'], person['last_name'], person['aliases'],
                       movies_as_productor=[movies['_id']])
            p.save_movies()
            m = Movies(movies['title'], movies['year'], productors=[person['_id']])
            m.save_people()
        elif args['like'] == 'actor':
            p = Person(person['first_name'], person['last_name'], person['aliases'],
                       movies_as_actor=[movies['_id']])
            p.save_movies()
            m = Movies(movies['title'], movies['year'], casting=[person['_id']])
            m.save_people()
        else:
            return {'message': 'people like what?'} , 400

        return ok, 201

        
