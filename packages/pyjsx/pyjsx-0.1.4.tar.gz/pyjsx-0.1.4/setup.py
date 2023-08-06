
cfg = {
    'name': 'pyjsx',
    'version':'0.1.4',
    'description':'Extendscript to Python bridge',
    'license':'GNU',
    'long_description':'',
    'author':'Yahia Boudah',
    'author_email':'yahiabouda@hotmail.com',
    'url':'',
    'packages':['pyes'],
    'install_requires':[],
    'scripts':[]
}
with open('README.md', 'r') as R: cfg['long_description'] = R.read()

from setuptools import setup
setup(**cfg)