from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Extra math functions'
LONG_DESCRIPTION = 'A package that gives you many math functions that are not in the math module.'

# Setting up
setup(
    name="mathextra",
    version=VERSION,
    author="TheCoder1001 (Atharv Baluja)",
    author_email="<thecoder1001yt@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['math'],
    keywords=['python', 'math', 'useful math functions'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
