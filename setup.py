from setuptools import setup, find_packages

setup(
    name="status_bot",
    version="v2.0.1",
    author="Rui Pires",
    author_email="rpires.projects@gmail.com",
    keywords="polling cli services cvs",
    packages=find_packages(),
    scripts=['status_bot/__main__.py'],
    required=[
        "requests",
        "pyyaml"
    ]
)
