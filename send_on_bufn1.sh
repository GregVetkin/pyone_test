#!/bin/bash

ssh u@bufn1 "sudo rm -r ~/brest/api/pyone/"
scp -r ~/Документы/Projects/pyone_test u@bufn1:/home/u/brest/api/
ssh u@bufn1 "sudo chmod 777 -R ~/brest/api/pyone_test" 
ssh u@bufn1 "sudo rm -rf ~/brest/api/pyone_test/.venv"
ssh u@bufn1 "sudo mv ~/brest/api/pyone_test ~/brest/api/pyone"
# ssh u@bufn1 "~/brest/pyone_test/prepare.sh"
