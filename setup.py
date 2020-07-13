import os

from setuptools import find_packages, setup


setup(
    name='hackernews',
    entry_points={
        'console_scripts': [
            'hackernews=hackernews.cli:cli',
        ],
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
