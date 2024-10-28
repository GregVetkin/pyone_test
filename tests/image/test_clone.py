import pytest

from api                import One
from pyone              import OneServer, OneActionException, OneNoExistsException, OneException
from utils              import get_brestadm_auth, run_command


URI                 = "http://localhost:2633/RPC2"
BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(URI, BRESTADM_AUTH)



ERROR_GETTING_IMAGE     = "Error getting image"




def test_image_not_exist():
    pass


def test_datastore_not_exist():
    pass


def test_name_is_taken():
    pass


def test_only_image_datastore_support():
    pass


def test_clone_into_the_same_datastore():
    pass


def test_clone_into_another_datastore():
    pass

