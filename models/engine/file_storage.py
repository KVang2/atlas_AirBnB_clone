#!/usr/bin/python3
import json
"""
This class represent the serialization and
deserialization of a file
"""


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (__file_path)."""
        serialized_objects = {}
        for key, obj in self.__objects.items():
            serialized_objects[key] = obj.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        from models.base_model import BaseModel
        try:
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
                for key, obj_dict in data.items():
                    class_name, obj_id = key.split('.')
                    # Dynamically create an instance of the class
                    obj_instance = globals().get(class_name)

                    if issubclass(globals().get(class_name), BaseModel):
                        obj_instance = globals().get(class_name)(**obj_dict)
                        self.__objects[key] = obj_instance
                    else:
                        print("Error: Class '{}' not found.".format(class_name))
        except FileNotFoundError:
            pass  # No exception should be raised if the file doesn't exist
