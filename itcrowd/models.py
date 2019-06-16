from itcrowd import  *


class Person:
    def __init__(self, first_name: str, last_name: str,
                 aliases: str, movies_as_actor: list = [],
                 movies_as_director: list = [],
                 movies_as_productor: list = []) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.aliases = aliases
        self.movies_as_actor = movies_as_actor
        self.movies_as_director = movies_as_director
        self.movies_as_productor = movies_as_productor


    def save(self) -> int:
        if not db.person.find({'last_name': self.last_name,
                               'first_name': self.first_name,
                               'aliases': self.aliases}).count():
            db.person.insert(self.to_json())
            return 0
        else:
            return -1  # return -1 if the person exist


    def to_json(self) -> dict:
        return {
                'last_name': self.last_name,
                'first_name': self.first_name,
                'aliases': self.aliases,
                'movies_as_actor': self.movies_as_actor, 
                'movies_as_director': self.movies_as_director,
                'movies_as_productor': self.movies_as_productor
            }

    def save_movies(self) -> int:
        person = db.person.find({
                "last_name": self.last_name,
                "first_name": self.first_name,
                "aliases": self.aliases
            })
        person = person[0]
        
        if person:
            self.movies_as_actor += person['movies_as_actor']
            self.movies_as_director += person['movies_as_director']
            self.movies_as_productor += person['movies_as_productor']
            self._update()
            return 0
        else:
            return -1  # Do you want to add movies a not exisiting person

    def _update(self) -> None:
        db.person.update({
                'last_name': self.last_name,
                'first_name': self.first_name,
                'aliases': self.aliases
                }, {'last_name': self.last_name,
                    'first_name': self.first_name,
                    'aliases': self.aliases,
                    'movies_as_actor': self.movies_as_actor,
                    'movies_as_director': self.movies_as_director,
                    'movies_as_productor': self.movies_as_productor})


class Movies:
    def __init__(self, title: str, year: int,
                 casting: list = [],
                 directors: list = [],
                 productors: list = []):
        self.title = title
        self.casting = casting
        self.year = year
        self.directors = directors
        self.productors = productors


    def save(self) -> int:
        if not db.movies.find({'title': self.title,
                               'year': self.year}).count():
            db.movies.insert(self.to_json())
            return 0
        else:
            return -1  # return -1 if the Movies exist


    def to_json(self) -> dict:
        return {
                'title': self.title,
                'year': self.year,
                'casting': self.casting, 
                'directors': self.directors,
                'productors': self.productors
            }

    def save_people(self) -> int:
        movies = db.movies.find({
                'title': self.title,
                'year': self.year,
            })
        movies = movies[0]
        
        if movies:
            self.casting += movies['casting']
            self.directors += movies['directors']
            self.productors += movies['productors']
            self._update()
            return 0
        else:
            return -1  # Do you want to add movies a not exisiting person

    def _update(self) -> None:
        db.person.update({
                'title': self.title,
                'year': self.year,
                }, {'title': self.title,
                    'year': self.year,
                    'casting': self.casting,
                    'directors': self.directors,
                    'productors': self.productors})
