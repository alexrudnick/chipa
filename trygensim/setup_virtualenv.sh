#!/bin/bash

virtualenv -p /usr/bin/python3 venv
. venv/bin/activate

pip install --upgrade gensim
