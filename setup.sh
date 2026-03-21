#!/bin/bash
# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install rgbmatrix pkg 
# Source: https://github.com/hzeller/rpi-rgb-led-matrix?tab=readme-ov-file#python-support
sudo apt-get install python-dev-is-python3 python3-pil cython3
pip install git+https://github.com/hzeller/rpi-rgb-led-matrix

# Install other dependencies
python3 -m pip install --upgrade pip
pip3 install -U -r requirements.txt
sudo apt install ffmpeg

# Set up sudo alias
# Create aliases file if not exists
if [ ! -f ~/.bash_aliases ]; then touch ~/.bash_aliases; fi
echo "alias sudopy='sudo $(printenv VIRTUAL_ENV)/bin/python3'" >> ~/.bash_aliases
source ~/.bash_aliases