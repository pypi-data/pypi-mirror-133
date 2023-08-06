#! usr/bin/env python
# setup.py

import setuptools


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()


setuptools.setup(
    name="anarchychess",
    version="0.0.1",
    author="Jacob Lee",
    author_email="JLpython@outlook.com",
    description="A Python chess package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JLpython-py/AnarchyChess",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
    ],
    python_requires=">=3.6",
)
