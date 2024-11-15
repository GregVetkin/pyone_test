import pytest
from api                import One
from pyone              import OneNoExistsException, OneInternalException
from utils              import get_unic_name
from one_cli.datastore  import Datastore, datastore_exist
from one_cli.cluster    import Cluster, create_cluster
from config             import ADMIN_NAME





@pytest.fixture
def cluster():
    _id = create_cluster(get_unic_name())
    cluster = Cluster(_id)
    yield cluster
    cluster.delete()


# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_cluster_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.datastore.allocate(f"NAME={get_unic_name()}\nTM_MAD=ssh\nDS_MAD=fs", cluster_id=999999)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_creation(one: One):
    _id  = one.datastore.allocate(f"NAME={get_unic_name()}\nTM_MAD=ssh\nDS_MAD=fs")
    assert datastore_exist(_id)
    Datastore(_id).delete()


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_creation_xml(one: One):
    _id = one.datastore.allocate(f"<DATASTORE><NAME>{get_unic_name()}</NAME><TM_MAD>ssh</TM_MAD><DS_MAD>fs</DS_MAD></DATASTORE>")
    assert datastore_exist(_id)
    Datastore(_id).delete()


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_mandatory_params(one: One):

    with pytest.raises(OneInternalException):
        one.datastore.allocate("")

    with pytest.raises(OneInternalException):
        one.datastore.allocate(f"NAME={get_unic_name()}")
    
    with pytest.raises(OneInternalException):
        one.datastore.allocate(f"NAME={get_unic_name()}\nTM_MAD=ssh")

    with pytest.raises(OneInternalException):
        one.datastore.allocate(f"NAME={get_unic_name()}\nDS_MAD=fs")
        

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_mandatory_params_xml(one: One):

    with pytest.raises(OneInternalException):
        one.datastore.allocate("<DATASTORE></DATASTORE>")

    with pytest.raises(OneInternalException):
        one.datastore.allocate(f"""<DATASTORE><NAME>{get_unic_name()}</NAME></DATASTORE>""")
    
    with pytest.raises(OneInternalException):
        one.datastore.allocate(f"""<DATASTORE><NAME>{get_unic_name()}</NAME><TM_MAD>ssh</TM_MAD></DATASTORE>""")

    with pytest.raises(OneInternalException):
        one.datastore.allocate(f"""<DATASTORE><NAME>{get_unic_name()}</NAME><DS_MAD>fs</DS_MAD></DATASTORE>""")


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_datastore_create_with_certain_cluster(one: One, cluster: Cluster):
    _id  = one.datastore.allocate(f"NAME={get_unic_name()}\nTM_MAD=ssh\nDS_MAD=fs", cluster_id=cluster._id)
    datastore = Datastore(_id)
    assert datastore_exist(_id)
    assert cluster._id in datastore.info().CLUSTERS
    datastore.delete()

