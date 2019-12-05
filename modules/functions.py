""" This module regroups several functions used by the main program"""
import json


# function allowing to put any file in a dictionary
def json_to_dictionary(path):
    with open(path, 'r') as JSONData:
        json_dict = json.load(JSONData)
    return json_dict


# function saving our data in a json file
def dictionary_to_json(path, dictionary):
    with open(path, 'w') as JSONData:
        json.dump(dictionary, JSONData, indent=4, ensure_ascii=False)


# function getting the hashed password of a person
def get_password(dictionary, mail):
    for key, value in dictionary.items():
        if key == mail:
            val_dict = dict(value)
            return val_dict['password']
