import json
from setuptools import setup

with open('CONFIG', 'r')    as C: cfg = json.loads(C.read())
with open('README.md', 'r') as R: cfg['long_description'] = R.read()

setup(**cfg)