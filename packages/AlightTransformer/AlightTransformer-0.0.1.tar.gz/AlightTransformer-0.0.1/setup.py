from setuptools import setup, find_packages
import codecs
import os

setup(
    name="AlightTransformer",
    version="0.0.1",
    author="Pantea Ferdosian",
    author_email="pantea.ferdosian@alight.com",
    description="Question and answer table generator",
    pachages = find_packages(),
    keywords=['python', 'Q&A', 'Questgen', 'Question Answering'],
    py_modules = ["QGen"]

)