#!/bin/bash

PROJECT_SHELL_DIRECTORY=$(dirname "$(realpath "$0")")
PROJECT_DIRECTORY=$(dirname ${PROJECT_SHELL_DIRECTORY})
PROJECT_VENV_DIRECTORY="${PROJECT_DIRECTORY}/.venv/"
PROJECT_CONFIGS_DIRECTORY="${PROJECT_DIRECTORY}/config/"


PYTHON3_VENV_PACKAGE_NAME="python3-venv"
ASTRA_VERSION=$(cat /etc/astra/build_version)
BREST_VERSION=$(cat /etc/brest/build_version)




case $(echo ${ASTRA_VERSION} | head -c 3) in 
    "1.7")
        PIP_PACKAGES=("lxml==4.4.0" "pyone==6.10.0" "pytest")
        REPO_BRANCH="base-repository"
        ;;
    "1.8")
        PIP_PACKAGES=("pyone" "pytest")
        REPO_BRANCH="extended-repository"
        ;;
    *)
        echo "Под версию ALSE ${ASTRA_MAJOR_VERSION} не подготовлен скрипт"
        exit 1
        ;;
esac 




# Проверка существования пакета в текущих репозиториях
if ! sudo apt-cache policy ${PYTHON3_VENV_PACKAGE_NAME} | grep -Pq '(Кандидат|Candidate):\s*\d'; then
    REPO_LINE=$(cat /etc/apt/sources.list | grep -m 1 "https")
    echo "$REPO_LINE" | sed "s|\(deb [^ ]*/\)[^ ]*|\1${REPO_BRANCH}|g" | sudo tee -a /etc/apt/sources.list
    sudo apt update
fi




# Установка пакет venv для python и создание виртуальной среды в корне проекта
sudo apt install -y ${PYTHON3_VENV_PACKAGE_NAME} --allow-downgrades
python3 -m venv ${PROJECT_VENV_DIRECTORY}




# Обновление pip в виртуальной среде и установка нужных пакетов
source "${PROJECT_VENV_DIRECTORY}/bin/activate";    pip3 install --upgrade pip;             deactivate
source "${PROJECT_VENV_DIRECTORY}/bin/activate";    pip3 install "${PIP_PACKAGES[@]}";      deactivate




# Проброс в файл конфигурации версий AL и Brest
sed -i "s/^\(ASTRA_VERSION\s*=\s*\).*/\1\"${ASTRA_VERSION}\"/"    "${PROJECT_CONFIGS_DIRECTORY}/base.py"
sed -i "s/^\(BREST_VERSION\s*=\s*\).*/\1\"${BREST_VERSION}\"/"    "${PROJECT_CONFIGS_DIRECTORY}/base.py"




# Активирован ли RAFT в стенде
if sudo cat /etc/one/one.d/raft.conf | grep -E "^\s*SERVER_ID" | grep "\-1"; then
    IS_RAFT_ON="False"
else
    IS_RAFT_ON="True"
fi
sed -i "s/^\(RAFT_ENABLED\s*=\s*\).*/\1${IS_RAFT_ON}/"    "${PROJECT_CONFIGS_DIRECTORY}/base.py"



# Доменное имя
DOMAIN_NAME=$(hostname -h)
sed -i "s/^\(DOMAIN_NAME\s*=\s*\).*/\1\"${DOMAIN_NAME}\"/"    "${PROJECT_CONFIGS_DIRECTORY}/base.py"
