import os
import codecs
from setuptools import setup, find_packages

# get __version__ from _version.py
ver_file = os.path.join('specio', '_version.py')
with open(ver_file) as f:
    exec(f.read())

PACKAGES = find_packages()

CLASSIFIERS = ["Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved",
               "Operating System :: OS Independent",
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               "Topic :: Scientific/Engineering"]

description = "pyITK: a wrapper around ITK."
with codecs.open('README.rst', encoding='utf-8-sig') as f:
    long_description = f.read()

NAME = "pyITK"
MAINTAINER = "Guillaume Lemaitre"
MAINTAINER_EMAIL = "glemaitre58@gmail.com"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/glemaitre/pyITK"
DOWNLOAD_URL = ""
LICENSE = "BSD3"
AUTHOR = "Guillaume Lemaitre"
AUTHOR_EMAIL = "g.lemaitre58@gmail.com"
PLATFORMS = "OS Independent"
VERSION = __version__


opts = dict(name=NAME,
            maintainer=MAINTAINER,
            maintainer_email=MAINTAINER_EMAIL,
            description=DESCRIPTION,
            long_description=LONG_DESCRIPTION,
            url=URL,
            download_url=DOWNLOAD_URL,
            license=LICENSE,
            classifiers=CLASSIFIERS,
            author=AUTHOR,
            author_email=AUTHOR_EMAIL,
            platforms=PLATFORMS,
            version=VERSION,
            packages=PACKAGES,
            include_package_data=True)


if __name__ == '__main__':
    setup(**opts)
