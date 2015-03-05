try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'cloudtb',
    'author': 'Garrett Berg',
    'author_email': 'garrett@cloudformdesign.com',
    'version': '0.2.0',
    'packages': ['cloudtb'],
    'install_requires': [
        'six',
    ],
    'extras_require': {
        'data':  ['numpy', 'pandas'],
        'visual': ['ansicolors', 'bokeh'],
    },
    'description': "Open source methods to solve common problems",
    'url': "https://github.com/cloudformdesign/cloudtb"
}

setup(**config)
