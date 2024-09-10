#!/bin/bash

FROM_BRESTADM="sudo -u brestadm"
CREATE_TOKEN="oneuser token-create"
TOKEN_USER="oneadmin"
ADMIN_GROUP="brestadmins"
TOKEN_GROUP="--group ${ADMIN_GROUP}"





ssh u@bufn1 "${FROM_BRESTADM} ${CREATE_TOKEN} ${TOKEN_USER} ${TOKEN_GROUP}"