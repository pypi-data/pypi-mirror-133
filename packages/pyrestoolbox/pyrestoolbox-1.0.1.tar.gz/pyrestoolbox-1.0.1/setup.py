from setuptools import setup

import os

ROOT = os.path.abspath(os.path.dirname(__file__))

setup(
    name = 'pyrestoolbox',
    packages = ['pyrestoolbox'],
    version = '1.0.1',  # Ideally should be same as your GitHub release tag varsion
    description = 'pyResToolbox - A collection of Reservoir Engineering Utilities',
    long_description= (ROOT + '/README.rst'),
    #long_description_content_type = text/markdown,
    author = 'Mark W. Burgoyne',
    author_email = 'mark.w.burgoyne@gmail.com',
    url = 'https://github.com/mwburgoyne/pyResToolbox',
    download_url = 'https://github.com/mwburgoyne/pyResToolbox/archive/refs/tags/v1.0.0.tar.gz',
    keywords = ['restoolbox', 'petroleum', 'reservoir'],
    classifiers = [],
    install_requires=[
        'requests',
        'importlib; python_version == "2.6"',
    ],
)