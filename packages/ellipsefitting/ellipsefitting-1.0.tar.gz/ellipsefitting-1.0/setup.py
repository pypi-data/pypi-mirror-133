import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ellipsefitting",
    version="1.0",
    description="Least squares fitting of Ellipses",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ehtec/least-squares-ellipse-fitting",
    author="Elias Hohl",  # forked from Ben Hammel
    author_email="elias.hohl@ehtec.co",
    license="MIT",
    py_modules=['ellipse'],
    install_requires=["numpy"],
)
