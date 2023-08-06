import json
from setuptools import setup

with open('README.md', 'r') as R, open('SETUP.json', 'r') as S:
    cfg = json.loads(S.read())
    cfg["long_description"] = R.read()

setup(**cfg)