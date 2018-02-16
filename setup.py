#!/usr/bin/env python
# -*- coding: utf8 -*-
import nltk
import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install

class DevelopScript(develop):
    def run(self):
        develop.run(self)
        ntlk_install_packages()


class InstallScript(install):
    def run(self):
        install.run(self)
        ntlk_install_packages()


def ntlk_install_packages():
    print("Downloading nltk packages...")
    nltk.download('punkt')

setuptools.setup(
    name="zeeguu_web",
    version="0.1",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    author="Zeeguu Team",
    author_email="me@mir.lu",
    description="Basic Web Presence for Zeeguu",
    keywords="Zeeguu is an ecosystem which aims at accelerating second language acquisition",
    cmdclass={
        'develop': DevelopScript,
        'install': InstallScript,
    },
    dependency_links=[
        "git+https://github.com/mircealungu/zeeguu-core.git#egg=zeeguu",
        "git+https://github.com/mircealungu/Unified-Multilanguage-Reader.git#egg=umr",
        "git+https://github.com/mircealungu/practice-as-a-service.git#egg=zeeguu_exercises"
    ],
    install_requires=("flask>=0.10.1",
                      "Flask-SQLAlchemy",
                      "Flask-Assets",
                      "cssmin",
                      "zeeguu",
			"umr",
			"zeeguu_exercises")
)
