#!/bin/bash

ssh u@bufn1 "sudo rm -r ~/brest/pyone_refactor/"

scp -r ~/Документы/pyone_refactor/ u@bufn1:/home/u/brest/

ssh u@bufn1 "sudo chmod 777 -R ~/brest/pyone_refactor/" 

ssh u@bufn1 "sudo rm -rf ~/brest/pyone_refactor/.venv"
