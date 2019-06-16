# itcrowd
IT crowd  test

## Endpoints
  * ```/SayHello```
  * ```/GetAllPeople```
  * ```/GetPersonByAlias``` : ```/GetPersonByAlias/The%20Rock```
  * ```/GetPersonByFirstName```: ```/GetPersonByFirstName/Keanu```
  * ```/GetPersonByLastName```: ```/GetPersonByLastName/Reeves```
  * ```/Person```: ```{"first_name":[first_name], "last_name": [last_name], "alias":[alias]}```
  * ```/Movies```: ```{"title": [title], "year": [year]}```
  * ```/MovieList```
  * ```/GetMoviesByTitle```: ```/GetMoviesByTitle/Matrix```
  * ```/AddPersonToMovieAs```: ```{"alias": "Keanu", "like": "actor", "title": "The Matrix"}```

## API Rules
api.add_resource(SayHello, '/SayHello')
api.add_resource(GetAllPeople, '/GetAllPeople')
api.add_resource(GetPersonByAlias, '/GetPersonByAlias/<string:alias>')
api.add_resource(GetPersonByFirstName, '/GetPersonByFirstName/<string:first_name>')
api.add_resource(GetPersonByLastName, '/GetPersonByLastName/<string:last_name>')
api.add_resource(SetPerson, '/Person')
api.add_resource(SetMovies, '/Movies')
api.add_resource(GetMoviesByTitle, '/Movies/<string:title>')
api.add_resource(AddPersonToMovieAs, '/AddPersonToMovieAs')
api.add_resource(MoviesList, '/MoviesList')
  
## Authentication

Create a collection named ```authentication``` and add {"user": [username],"password": [password]}


## ISSUES / PR created meanwhile this test
* https://github.com/dcrosta/flask-pymongo/pull/130 -> https://github.com/dcrosta/flask-pymongo/commit/681993b559585c7d414d364b35bdb66181a6ff7d

# Why flask?

Becuase is a minimalist framework, and is was more easy and quickly develop this test.

# What modules used?

See ```requirements.txt``` :-)
