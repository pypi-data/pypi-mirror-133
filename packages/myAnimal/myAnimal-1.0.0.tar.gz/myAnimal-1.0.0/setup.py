from distutils.core import setup
import setuptools

setuptools.setup(name="myAnimal",
                version= "1.0.0",
                long_description= "dont install this",
                packages= setuptools.find_packages(exclude=['env']))