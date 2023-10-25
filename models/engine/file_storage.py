#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import shlex
from models.base_model import BaseModel
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City
from models.user import User


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        dictionary = {}
        if cls:
            dic = self.__objects
            for k in dic:
                spl = k.replace('.', ' ')
                spl = shlex.split(spl)
                if (spl[0] == cls.__name__):
                    dictionary[k] = self.__objects[k]
            return (dictionary)
        else:
            return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj:
            k = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[k] = obj

    def save(self):
        """Saves storage dictionary to file"""
        dic = {}
        for k, val in self.__objects.items():
            dic[k] = val.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as fl:
            json.dump(dic, fl)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, 'w', encoding="UTF-8") as fl:
                for k, val in (json.load(fl)).items():
                    val = eval(val["__class__"])(**val)
                    self.__objects[k] = val
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        delete an element existing
        """
        if obj:
            k = f"{obj.__class__.__name__}.{obj.id}"
            del self.__objects[k]

    def close(self):
        """
        reload
        """
        self.reload()
