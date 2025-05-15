#!/bin/bash

SCRIPT_DIR=$(dirname $(realpath "${BASH_SOURCE[0]}"))
PARENT_SCRIPT_DIR=$(dirname $SCRIPT_DIR)

ssh u@bufn1 "sudo rm -r ~/brest/api/pyone/"
scp -r $PARENT_SCRIPT_DIR u@bufn1:/home/u/brest/api/
ssh u@bufn1 "sudo chmod 777 -R ~/brest/api/pyone_test" 
ssh u@bufn1 "sudo rm -rf ~/brest/api/pyone_test/.venv"
ssh u@bufn1 "sudo mv ~/brest/api/pyone_test ~/brest/api/pyone"
