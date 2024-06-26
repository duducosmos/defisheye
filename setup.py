#!/usr/bin/env python3
# -*- Coding: UTF-8 -*-
import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="defisheye",
    license="Apache License 2.0",
    version='1.4.1',
    author='Eduardo S. Pereira',
    author_email='pereira.somoza@gmail.com',
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"": ["gui/*"]},
    description="Fast defisheye algorithm",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/duducosmos/defisheye",
    install_requires=["numpy",
                      "opencv-python",
                      "argcomplete",
                      'tqdm',
                      'pygubu',
                      'Pillow'
                      ],
    entry_points={"console_scripts": [
        "defisheye = defisheye.__main__:main",
        "defisheyeapp = defisheye.__main__:mainapp"]},
)
