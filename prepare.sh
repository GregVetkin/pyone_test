#!/bin/bash


function is_package_in_repos() {
    local PACKAGE_NAME="$1"

    if sudo apt-cache policy "${PACKAGE_NAME}" | grep "Кандидат" | grep "(отсутствует)" &>/dev/null; then
        return 1
    else
        return 0
    fi
}



function install_python_packages_in_venv_with_pip() {
    local VENV_DIR="$1"
    shift
    local PACKAGES=("$@")

    source "${VENV_DIR}/bin/activate"
    pip3 install "${PACKAGES[@]}"
    deactivate
}


function add_repository() {
    local REPO_BRANCH=$1
    local REPO_LINE=$(cat /etc/apt/sources.list | grep -m 1 "https")

    echo "$REPO_LINE" | sed "s|\(deb [^ ]*/\)[^ ]*|\1${REPO_BRANCH}|g" | sudo tee -a /etc/apt/sources.list

    sudo apt update
}




DIR=$(dirname "$(realpath "$0")")
VENV_DIR="${DIR}/.venv/"
PYTHON3_VENV_PACKAGE_NAME="python3-venv"

ASTRA_VERSION=$(head -c 3 /etc/astra_version)
BREST_VERSION=$(head -c 1 /etc/brest_version)


if [ $ASTRA_VERSION == "1.8" ]; then
    PIP_PACKAGES=("pyone" "pytest")
    REPO_BRANCH="extended-repository"
else
    PIP_PACKAGES=("lxml==4.4.0" "pyone==6.10.0" "pytest")
    REPO_BRANCH="base-repository"
fi






if ! is_package_in_repos "${PYTHON3_VENV_PACKAGE_NAME}"; then
    add_repository "$REPO_BRANCH"
fi



sudo apt install -y ${PYTHON3_VENV_PACKAGE_NAME} --allow-downgrades
python3 -m venv ${VENV_DIR}

source "${VENV_DIR}/bin/activate"; pip3 install --upgrade pip; deactivate
source "${VENV_DIR}/bin/activate"; pip3 install "${PIP_PACKAGES[@]}"; deactivate



sed -i "s/^\(ALSE_VERSION\s*=\s*\).*/\1${ASTRA_VERSION}/" "${DIR}/config.py"
sed -i "s/^\(BREST_VERSION\s*=\s*\).*/\1${BREST_VERSION}/" "${DIR}/config.py"