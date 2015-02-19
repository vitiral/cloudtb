try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'cloudtb',
    'version': '0.1',
    'packages': ['cloudtb'],
    'install_requires': [
    ],
    'description': "Open source methods to solve common problems",
    'url': "https://github.com/cloudformdesign/cloudtb"
}

setup(**config)
