#!/usr/bin/python3

""" New engine DBStorage """
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ New storage engine """
    __engine = None
    __session = None

    def __init__(self):
        username = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(username, password, host,
                                              database), pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session depending on class name """
        all_objs = {}
        if cls:
            if isinstance(cls, str):
                cls = globals().get(cls, None)
            query_result = self.__session.query(cls).all()
            for obj in query_result:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                all_objs[key] = obj
        else:
            model_classes = [Amenity, City, Place, Review, State, User]
            for model_class in model_classes:
                query_result = self.__session.query(model_class).all()
                for obj in query_result:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    all_objs[key] = obj
        return all_objs

    def new(self, obj):
        """ Adds the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commits all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes from the current database session """
        if obj:
            self.session.delete(obj)

    def reload(self):
        """ Reloads current database """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def close(self):
        """ Calls remove method on private session attribute """
        self.__session.close()
