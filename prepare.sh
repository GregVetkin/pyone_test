#!/bin/bash


function is_package_in_repos() {
    local PACKAGE_NAME="$1"

    if sudo apt show "${PACKAGE_NAME}" &>/dev/null; then
        return 0
    else
        return 1
    fi
}


function install_package() {
    local PACKAGE_NAME="$1"

    if sudo apt install "${PACKAGE_NAME}" -y &>/dev/null; then
        return 0
    else
        return 1
    fi
}


function create_python_venv() {
    local VENV_PATH="$1"

    python3 -m venv ${VENV_PATH}    &>/dev/null
}


function install_python_packages_in_venv_with_pip() {
    local VENV_DIR="$1"
    shift
    local PACKAGES=("$@")

    source "${VENV_DIR}/bin/activate"
    pip3 install "${PACKAGES[@]}" &>/dev/null
    deactivate
}


if ! is_package_in_repos "python3-venv"; then
    echo "Нет пакета в репозитории, отмена"
    exit 1
fi


install_package "python3-venv"
create_python_venv ~/pyone_test/.venv/
install_python_packages_in_venv_with_pip ~/pyone_test/.venv/ "lxml==4.4.0" "pyone"

