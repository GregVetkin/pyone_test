import pytest

from api                import One
from pyone              import OneNoExistsException
from utils              import get_user_auth, get_unic_name
from one_cli.datastore  import Datastore, datastore_exist
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


IMAGE_DS_TEMPLATE = f"""
    NAME   = {get_unic_name()}
    TYPE   = IMAGE_DS
    TM_MAD = ssh
    DS_MAD = fs
"""
FILE_DS_TEMPLATE = f"""
    NAME   = {get_unic_name()}
    TYPE   = FILE_DS
    TM_MAD = ssh
    DS_MAD = fs
"""
SYSTEM_DS_TEMPLATE = f"""
    NAME   = {get_unic_name()}
    TYPE   = SYSTEM_DS
    TM_MAD = ssh
"""


# =================================================================================================
# TESTS
# =================================================================================================
# ToDo:
# 1) Кластер
# 2) Передача кастомных параметров шаблона
# 3) Невалидные параметры в шаблоне
# 4) Проверка обязательных параметров
# 5) Проверка xml шаблона



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_cluster_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.datastore.allocate(IMAGE_DS_TEMPLATE, cluster_id=999999)



@pytest.mark.parametrize("valid_template", [IMAGE_DS_TEMPLATE, FILE_DS_TEMPLATE, SYSTEM_DS_TEMPLATE])
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_create_datastore(one: One, valid_template: str):
    datastore_id  = one.datastore.allocate(valid_template)
    datastore     = Datastore(datastore_id)
    assert datastore_exist(datastore_id) == True
    datastore.delete()

