import os
from ..exceptions.file_except import KeyValueMismatchError
from typing import List, Dict


READ = 'r'
KEY_LINE_POS = 0
VALUE_LINE_POS = 1
SEPERATOR = ","


# File: Handles operations within files
class File():

    def __init__(self, name):
        self._name = name


    # exists(): Checks if a file exits
    def exists(self) -> bool:
        return bool(os.path.exists(self._name))

    # name(): Getter for '_name'
    @property
    def name(self):
        return self._name


    # name(new_name): Setter for '_name'
    @name.setter
    def name(self, new_name: str):
        self._name = new_name


    # read_lines(): Reads all the lines in a file
    def read_lines(self) -> List[str]:
        account = open(self._name, READ)

        account.seek(0)
        file_source = account.readlines()
        account.close()
        return file_source


    # dict_read(): Reads the lines in a file assuming they are formatted as a
    #   dictionary
    # requires: there are same number of keys and values
    # note: the list of keys is in the first line while the list of values are
    #   in the second value
    def dict_read(self) -> Dict[str, str]:
        lines = self.read_lines()
        keys = lines[KEY_LINE_POS]
        values = lines[VALUE_LINE_POS]

        keys = keys.split(SEPERATOR)
        values = values.split(SEPERATOR)

        result = {}
        key_size = len(keys)
        value_size = len(values)

        # raise exception if the keys and values do not match
        if (key_size != value_size):
            raise KeyValueMismatchError(key_size, value_size)

        for i in range(key_size):
            result[keys[i].strip()] = values[i].strip()

        return result


    # remove(): Removes the file
    def remove(self):
        try:
            os.remove(self._name)
        except OSError as error:
            print(error)
            print("File path can not be removed")
