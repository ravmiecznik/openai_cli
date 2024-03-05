#!/bin/bash
env=OPENAI &&
python3 -m venv $env &&
ln -sf $PWD/chatgpt.py $PWD/$env/bin/chatgpt &&
ln -sf $PWD/.token $PWD/$env/bin/.token &&
source $env/bin/activate &&
python -m pip install openai==0.28 &&
pip install openai --upgrade 
