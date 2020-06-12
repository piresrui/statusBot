from setuptools import setup, find_packages

setup(
    name="statusBot",
    version="v1.1",
    author="Rui Pires",
    author_email="rpires.projects@gmail.com",
    keywords="polling cli services cvs",
    packages=find_packages(),
    required=[
        "requests"
    ]
)
