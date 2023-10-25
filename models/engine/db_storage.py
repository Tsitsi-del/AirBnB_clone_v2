#!/usr/bin/python3
""" sqlalchemy class """
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from os import getenv
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """
    tables in environment
    """
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
                        f'mysql+mysqldb://{user}:{passwd}@{host}/{db}',
                        pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.engine)

    def all(self, cls=None):
        """
        returns a dictionary of __object
        """

        obj_dic = {}

        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for element in query:
                k = f"{type(element).__name__}.{element.id}"
                obj_dic[k] = element
        else:
            list_class = [State, City, User, Place, Review, Amenity]
            for cl in list_class:
                query = self.__session.query(cl)
                for element in query:
                    k = "{}.{}".format(type(element).__name__, element.id)
                    obj_dic[k] = element
        return (obj_dic)

    def new(self, obj):
        """
        add element in table
        """
        self.__session.add(obj)

    def save(self):
        """
        save change on the database
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete element in table
        """
        if obj:
            self.session.delete(obj)

    def reload(self):
        """
        create all table in the database
        """
        Base.metadata.create_all(self.__engine)
        ses = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(ses)
        self.__session = Session()

    def close(self):
        """
        removes session
        """
        self.__session.close()
