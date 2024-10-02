import pyone
import pytest
from api    import One
from pyone  import OneServer



def test_version_for_brestusers():
    URL     = "http://bufn1.brest.local:2633/RPC2"
    one = pyone.OneServer(URL, "brestadm:ca62add7b4897b9e4e8a527ce2dfc63eafe83fd7a4401102bf13be0423c7ffe2")
    version = one.system.version()
    assert version == "6.0.0.2"

def test_version_for_brestadmins():
    assert True



