class DictList:
    """
    Wrapper class that acts like a dict whose values are lists.
    """

    def __init__(self):
        """
        Initializes the class
        """
        self._data = dict()

    def __getitem__(self, item):
        """
        Gets the list of the specified item. An empty list is created if the item is unknonw.
        :param item: the item whose lists is returned
        :return: the list of the specified item
        """
        if not self._data.has_key(item):
            self._data[item] = list()
        return self._data[item]

    def __delitem__(self, key):
        """
        Deletes the specified key in every list
        :param key: the key to be deleted in every list
        """
        for value in self._data.values():
            del value[key]

    def __delslice__(self, i, j):
        """
        Deletes the specified slice in every list
        :param i: starting key
        :param j: ending key
        """
        for value in self._data.values():
            del value[i:j]

    def keys(self):
        """
        Gets the keys of the dictionary
        :return: the keys
        """
        return self._data.keys()
