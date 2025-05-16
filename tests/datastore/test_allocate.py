import pytest
import pyone
from api          import One
from utils.other  import get_unic_name






def test_cluster_not_exist(one: One):
    template    = f"NAME={get_unic_name()}\nTM_MAD=ssh\nDS_MAD=fs"
    cluster_id  = 999999

    with pytest.raises(pyone.OneNoExistsException):
        one.datastore.allocate(template, cluster_id)



def test_datastore_creation(one: One):
    tm_mad   = "ssh"
    ds_mad   = "fs"
    ds_name  = get_unic_name()
    template = f"NAME={ds_name}\nTM_MAD={tm_mad}\nDS_MAD={ds_mad}"

    datastore_id = one.datastore.allocate(template)

    ds_info = one.datastore.info(datastore_id)
    assert ds_info.TM_MAD == tm_mad
    assert ds_info.DS_MAD == ds_mad
    assert ds_info.NAME   == ds_name

    one.datastore.delete(datastore_id)



def test_datastore_creation_xml(one: One):
    tm_mad   = "dummy"
    ds_mad   = "dummy"
    ds_name  = get_unic_name()
    template = f"<DATASTORE><NAME>{ds_name}</NAME><TM_MAD>{tm_mad}</TM_MAD><DS_MAD>{ds_mad}</DS_MAD></DATASTORE>"

    datastore_id = one.datastore.allocate(template)

    ds_info = one.datastore.info(datastore_id)
    assert ds_info.TM_MAD == tm_mad
    assert ds_info.DS_MAD == ds_mad
    assert ds_info.NAME   == ds_name

    one.datastore.delete(datastore_id)



def test_mandatory_params(one: One):

    with pytest.raises(pyone.OneInternalException):
        one.datastore.allocate("")

    with pytest.raises(pyone.OneInternalException):
        one.datastore.allocate(f"NAME={get_unic_name()}")
    
    with pytest.raises(pyone.OneInternalException):
        one.datastore.allocate(f"NAME={get_unic_name()}\nTM_MAD=ssh")

    with pytest.raises(pyone.OneInternalException):
        one.datastore.allocate(f"NAME={get_unic_name()}\nDS_MAD=fs")
        


def test_mandatory_params_xml(one: One):

    with pytest.raises(pyone.OneInternalException):
        one.datastore.allocate("<DATASTORE></DATASTORE>")

    with pytest.raises(pyone.OneInternalException):
        one.datastore.allocate(f"""<DATASTORE><NAME>{get_unic_name()}</NAME></DATASTORE>""")
    
    with pytest.raises(pyone.OneInternalException):
        one.datastore.allocate(f"""<DATASTORE><NAME>{get_unic_name()}</NAME><TM_MAD>ssh</TM_MAD></DATASTORE>""")

    with pytest.raises(pyone.OneInternalException):
        one.datastore.allocate(f"""<DATASTORE><NAME>{get_unic_name()}</NAME><DS_MAD>fs</DS_MAD></DATASTORE>""")



def test_certain_cluster(one: One, dummy_cluster):
    cluster_id   = dummy_cluster
    template     = f"NAME={get_unic_name()}\nTM_MAD=dummy\nDS_MAD=dummy"

    datastore_id = one.datastore.allocate(template, cluster_id)

    ds_info = one.datastore.info(datastore_id)
    assert cluster_id in ds_info.CLUSTERS.ID 

    one.datastore.delete(datastore_id)

