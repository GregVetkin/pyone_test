import pytest

from pyone              import OneServer
from api                import One
from one_cli.datastore  import Datastore, create_ds_by_tempalte
from one_cli.image      import Image, create_image_by_tempalte, image_exist
from one_cli.group      import Group, create_group
from one_cli.user       import User, create_user
from config             import API_URI



@pytest.fixture
def one(request):
    user_auth   = request.param
    session     = OneServer(API_URI, user_auth)
    yield One(session)


@pytest.fixture
def datastore(request):
    ds_id = create_ds_by_tempalte(request.param)
    ds    = Datastore(ds_id)

    yield ds

    ds.delete()


@pytest.fixture
def image(request, datastore: Datastore):
    image_id = create_image_by_tempalte(datastore._id, request.param)
    image    = Image(image_id)

    yield image

    if not image_exist(image._id):
        return

    if image.info().LOCK is not None:
        image.unlock()

    image.wait_ready_status()
    image.delete()


@pytest.fixture
def user(request):
    user_name = request.param
    user_id   = create_user(user_name)
    user      = User(user_id)

    yield user

    user.delete()


@pytest.fixture
def group(request):
    group_name  = request.param
    group_id    = create_group(group_name)
    group       = Group(group_id)

    yield group

    group.delete()

