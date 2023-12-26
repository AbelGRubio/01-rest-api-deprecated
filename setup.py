from setuptools import setup, find_packages
from src.api import __version__


with open('requirements.txt') as f:
    requirements = f.readlines()


with open("README.md", 'r') as f:
    long_description = f.read()


setup(
    name='REST api',
    version=__version__,
    author='agrubio',
    author_email="agrubio",
    description='This package is made for an example of REST API.',
    url='https://github.com/AbelGRubio/01-rest-api.git',
    keywords='development, setup, setuptools',
    python_requires='>=3.5',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['api', 'api.*']),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # include_package_data=True,
    # package_data={'': ['data/*.csv', 'data/*.txt']},
)
