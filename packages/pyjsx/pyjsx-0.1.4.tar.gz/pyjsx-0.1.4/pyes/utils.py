# Utils

# imports:
#   json (data ser/deser)
#   sys  (path append)
#   os   (path operations)
import json, os, sys

class Utils():

    @classmethod
    def file_name(self, pp):
        return '.'.join(pp.split('/')[-1].split('.')[0:-1])

    @classmethod
    def get_user(self):
        return os.path.split(os.path.expanduser('~'))[-1]

class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__