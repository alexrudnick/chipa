#!/bin/bash

virtualenv -p /usr/bin/python3 venv
. venv/bin/activate

pip install numpy
pip install scipy
pip install scikit-learn
pip install pyyaml
pip install https://github.com/nltk/nltk/tarball/develop
## make sure we have sentence segmenter models
## python3 -m nltk.downloader punkt
