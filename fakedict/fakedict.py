import json

class FakeDict(object):
    def __init__(self, getter, setter, key_getter, del_item = None):
        self._getter = getter
        self._setter = setter
        self._key_getter = key_getter
        self._del_item = del_item
    def keys(self):
        return self._key_getter()
    def __iter__(self):
        return self.keys().__iter__()
    def __contains__(self, name):
        return name in self.keys()
    def __getitem__(self, name):
        return self._getter(name)
    def __setitem__(self, name, value):
        return self._setter(name, value)
    def __delitem__(self, name):
        if self._del_item == None:
            raise Exception("Cannot delete items from this dictionary")
        else:
            self._del_item(name)
    def dict(self):
        return {str(key): self[key] for key in self.keys()}
    def iteritems(self):
        return self.dict().iteritems()
    def __str__(self):
        return str(self.dict())

class JSONFile(FakeDict):
    def __init__(self, filePath):
        self.filePath = filePath
        FakeDict.__init__(self, self.getter, self.setter, self.key_getter, self.del_item)

    def dict(self):
        output = {}
        try:
            with open(self.filePath,'r') as inFile:
                output = json.load(inFile)
        except (ValueError, IOError):
            with open(self.filePath, 'w') as outFile:
                json.dump(output, outFile)
        return output

    def _save_dict(self, d):
        with open(self.filePath, 'w') as f:
            json.dump(d, f)

    def getter(self, name):
        return self.dict()[name]

    def setter(self, name, value):
        values = self.dict()
        values[name] = value
        self._save_dict(values)

    def key_getter(self):
        return self.dict().keys()

    def del_item(self, name):
        values = self.dict()
        del values[name]
        self._save_dict(values)

class CollectionDict(FakeDict):
    def __init__(self, collection,
            col_key_getter = lambda item: item[0],
            col_value_getter = lambda item: item[1],
            col_value_setter = None,
            col_initializer = lambda name, value: [name, value]):
        self.col_key_getter = col_key_getter
        self.col_value_getter = col_value_getter
        self.col_value_setter = col_value_setter if col_value_setter != None else self._default_setter
        self.col_initializer = col_initializer
        self.collection = collection
        FakeDict.__init__(self, self.getter, self.setter, self.key_getter, self.del_item)

    def _find_index(self, name):
        keys = self.key_getter()
        if name not in keys:
            raise KeyError(name)
        return self.key_getter().index(name)

    def _find_item(self, name):
        return self.collection[self._find_index(name)]

    def getter(self, name):
        return self.col_value_getter(self._find_item(name))

    def setter(self, name, value):
        item = None
        try:
            item = self._find_item(name)
            self.col_value_setter(item, value)
        except KeyError:
            item = self.col_initializer(name, value)
            self.collection.append(item)

    def _default_setter(self, item, value):
        item[1] = value

    def key_getter(self):
        return [self.col_key_getter(item) for item in self.collection]

    def del_item(self, name):
        self.collection.pop(self._find_index(name))

