import json
import os


class Error(Exception):
    """Base error class with exception as the inheritance"""


class keyAlreadyExists(Error):
    """The key you tried to add already exists"""


class keyDoesnotExist(Error):
    """The key you tried to add already exists"""


class KPDBL(object):
    def __init__(self, location, autocommit=False):
        self.location = os.path.expanduser(location)
        self.load(location)
        self.autocommit = autocommit

    def load(self, location):
        if os.path.exists(location):
            self._load()
        else:
            self.db = {}
            self.dumpdb()
        return True

    def _load(self):
        self.db = json.load(open(self.location, 'r'))

    def dumpdb(self):
        try:
            json.dump(self.db, open(self.location, 'w+'))
            return True
        except:
            return False

    def add(self, name, value):
        if self.does_key_exist(name):
            raise keyAlreadyExists("The key already exists")
        else:
            self.db[name] = value
            if self.autocommit:
                self.commit()

    def set(self, name, value):
        if not name in list(self.db.keys()):
            raise keyDoesnotExist("Key does not exist in the database")
        else:
            self.db[name] = value
            if self.autocommit:
                self.commit()

    def delete(self, name):
        if not self.does_key_exist(name):
            raise keyDoesnotExist("Key does not exist in the database")
        else:
            self.db.pop(name)
            if self.autocommit:
                self.commit()

    def get(self, name):
        if not self.does_key_exist(name):
            raise keyDoesnotExist("Key does not exist in the database")
        else:
            return self.db[name]

    def get_all(self):
        return (list(self.db.keys()), list(self.db.values()))

    def commit(self):
        with open(self.location, 'r+') as f:
            f.truncate()
            f.write(json.dumps(self.db))

    def add_or_set(self, name, value):
        self.db[name] = value
        if self.autocommit:
            self.commit()

    def does_key_exist(self, key):
        if key in list(self.db.keys()):
            return True
        else:
            return False
