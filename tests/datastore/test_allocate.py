import pytest
import pyone
import random

from api          import One
from utils.other  import get_unic_name






def test_cluster_not_exist(one: One):
    template    = f"NAME={get_unic_name()}\nTM_MAD=ssh\nDS_MAD=fs"
    cluster_id  = random.randint(9999, 999999)

    with pytest.raises(pyone.OneNoExistsException):
        one.datastore.allocate(template, cluster_id)



def test_default_cluster(one: One):
    tm_mad      = "ssh"
    ds_mad      = "fs"
    ds_name     = get_unic_name()
    cluster_id  = -1
    template    = f"NAME={ds_name}\nTM_MAD={tm_mad}\nDS_MAD={ds_mad}"

    datastore_id = one.datastore.allocate(template, cluster_id)

    ds_info = one.datastore.info(datastore_id, False)
    assert ds_info.TM_MAD == tm_mad
    assert ds_info.DS_MAD == ds_mad
    assert ds_info.NAME   == ds_name
    assert 0 in ds_info.CLUSTERS.ID
    one.datastore.delete(datastore_id)



def test_specific_cluster(one: One, dummy_cluster):
    cluster_id   = dummy_cluster
    template     = f"NAME={get_unic_name()}\nTM_MAD=dummy\nDS_MAD=dummy"
    datastore_id = one.datastore.allocate(template, cluster_id)

    ds_info = one.datastore.info(datastore_id, False)
    assert cluster_id in ds_info.CLUSTERS.ID 

    one.datastore.delete(datastore_id)





def test_allocate_by_xml(one: One):
    tm_mad   = "dummy"
    ds_mad   = "dummy"
    ds_name  = get_unic_name()
    template = f"<DATASTORE><NAME>{ds_name}</NAME><TM_MAD>{tm_mad}</TM_MAD><DS_MAD>{ds_mad}</DS_MAD></DATASTORE>"
    cluster_id = -1
    datastore_id = one.datastore.allocate(template, cluster_id)

    ds_info = one.datastore.info(datastore_id, False)
    assert ds_info.TM_MAD == tm_mad
    assert ds_info.DS_MAD == ds_mad
    assert ds_info.NAME   == ds_name

    one.datastore.delete(datastore_id)



def test_mandatory_params(one: One):
    cluster_id = -1

    with pytest.raises(pyone.OneInternalException):
        one.datastore.allocate("", cluster_id)

    with pytest.raises(pyone.OneInternalException):
        one.datastore.allocate(f"NAME={get_unic_name()}", cluster_id)
    
    with pytest.raises(pyone.OneInternalException):
        one.datastore.allocate(f"NAME={get_unic_name()}\nTM_MAD=ssh", cluster_id)

    with pytest.raises(pyone.OneInternalException):
        one.datastore.allocate(f"NAME={get_unic_name()}\nDS_MAD=fs", cluster_id)
        


