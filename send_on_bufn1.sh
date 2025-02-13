#!/bin/bash

ssh u@bufn1 "sudo rm -r ~/brest/pyone_test/"
scp -r ~/Документы/Projects/pyone_test u@bufn1:/home/u/brest/ 
ssh u@bufn1 "sudo chmod 777 -R ~/brest/pyone_test" 
ssh u@bufn1 "sudo rm -rf ~/brest/pyone_test/.venv"
# ssh u@bufn1 "~/brest/pyone_test/prepare.sh"
