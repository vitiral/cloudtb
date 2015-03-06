try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from cloudtb import __version__

config = {
    'name': 'cloudtb',
    'author': 'Garrett Berg',
    'author_email': 'garrett@cloudformdesign.com',
    'version': __version__,
    'packages': ['cloudtb'],
    'license': 'MIT',
    'install_requires': [
        'six',
    ],
    'extras_require': {
        'data':  ['numpy', 'pandas'],
        'visual': ['ansicolors', 'bokeh'],
        'platform': ['psutil'],
    },
    'description': "Open source methods to solve common problems",
    'url': "https://github.com/cloudformdesign/cloudtb",
    'classifiers': [
        # 'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Text Processing :: General',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
}

setup(**config)
