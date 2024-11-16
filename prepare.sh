#!/bin/bash


function is_package_in_repos() {
    local PACKAGE_NAME="$1"

    if sudo apt-cache policy "${PACKAGE_NAME}" | grep "Кандидат" | grep "(отсутствует)" &>/dev/null; then
        return 1
    else
        return 0
    fi
}


function install_package() {
    local PACKAGE_NAME="$1"

    if sudo apt install "${PACKAGE_NAME}" -y ; then
        return 0
    else
        return 1
    fi
}


function create_python_venv() {
    local VENV_PATH="$1"

    python3 -m venv ${VENV_PATH}
}


function install_python_packages_in_venv_with_pip() {
    local VENV_DIR="$1"
    shift
    local PACKAGES=("$@")

    source "${VENV_DIR}/bin/activate"
    pip3 install "${PACKAGES[@]}"
    deactivate
}


function add_base_repository() {
    local BUILD_VERSION=$(cat /etc/astra/build_version)

    local MAJOR=$(echo "${BUILD_VERSION}" | cut -d'.' -f1)
    local MINOR=$(echo "${BUILD_VERSION}" | cut -d'.' -f2)
    local PATCH=$(echo "${BUILD_VERSION}" | cut -d'.' -f3)

    local REPO_DATA="deb ${REPO}/${MAJOR}.${MINOR}/${MAJOR}.${MINOR}.${PATCH}/_REPO/base-repository ${MAJOR}.${MINOR}_x86-64 main contrib non-free"

    echo "${REPO_DATA}" | sudo tee -a /etc/apt/sources.list
    sudo apt update
}



REPO="https://releases.devos.astralinux.ru/stable/"

DIR=$(dirname "$(realpath "$0")")
PACKAGE="python3-venv"
VENV_DIR="${DIR}/.venv/"
PIP_PACKAGES=("lxml==4.4.0" "pyone" "pytest")




if ! is_package_in_repos "${PACKAGE}"; then
    add_base_repository
fi

if ! is_package_in_repos "${PACKAGE}"; then
    echo "Пакет ${PACKAGE} не найден после добавления base репозитория."
    echo "Добавьте корретный репозиторий и перезапустите скрипт."
    exit 1
fi


install_package "${PACKAGE}"
create_python_venv $VENV_DIR
source "${VENV_DIR}/bin/activate"; pip3 install --upgrade pip; deactivate
install_python_packages_in_venv_with_pip $VENV_DIR "${PIP_PACKAGES[@]}"

