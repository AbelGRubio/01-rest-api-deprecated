from setuptools import setup, find_packages
from src.iniciativas import __version__


with open('requirements.txt') as f:
    requirements = f.readlines()


with open("README.md", 'r') as f:
    long_description = f.read()


setup(
    name='cedro',
    version=__version__,
    author='Brainy Inteligencia Semántica',
    author_email="info@brainy.technology",
    description='This package is made for iniciativas spider.',
    url='https://gitlab.brainyinteligencia.com/brainy/scrapper-iniciativas.git',
    keywords='development, setup, setuptools',
    python_requires='>=3.5',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['iniciativas', 'iniciativas.*']),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # include_package_data=True,
    # package_data={'': ['data/*.csv', 'data/*.txt']},
)
