#!/bin/bash


sudo apt-get install python3-venv -y  #&>/dev/null


mkdir -m 777 ~/one_api && cd ~/one_api     #&>/dev/null


python3 -m venv ~/one_api/.venv               #&>/dev/null


. .venv/bin/activate && pip3 install lxml==4.4.0
. .venv/bin/activate && pip3 install pyone

