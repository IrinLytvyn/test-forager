"""File that helps to create a package."""
from setuptools import find_packages, setup

setup(
    name='spotify-data-manipulation',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)
