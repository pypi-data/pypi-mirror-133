import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "example_proejct",
    version = "0.0.1",
    author = "hyeonykim ",
    author_email = "hyeonykim@gmail.com",
    description = ("test"),
    license = "None",
    keywords = "example",
    url = "http://example.com",
    packages=['example', 'tests'],
    long_description=read('README'),
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)
