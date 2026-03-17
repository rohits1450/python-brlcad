from .db import Database

def open(path):
    return Database(path)
