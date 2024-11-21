import pytest
import random
from typing     import Tuple
from pyone      import OneNoExistsException, OneException



def _rights_as_tuple(one_object):
    _ = one_object.info().PERMISSIONS
    return (_.OWNER_U, _.OWNER_M, _.OWNER_A, _.GROUP_U, _.GROUP_M, _.GROUP_A, _.OTHER_U, _.OTHER_M, _.OTHER_A)



def _rights_tuples_list(n: int = 9):
    result = []

    for i in range(1, n + 1):
        t = tuple(1 if _ < i else 0 for _ in range(n))
        result.append(t)

    for i in range(n + 1):
        t = tuple(0 if _ < i else 1 for _ in range(n))
        result.append(t)

    return result



def chmod_if_not_exist__test(api_method):
    with pytest.raises(OneNoExistsException):
        api_method.chmod(999999)


def chmod__test(api_method, one_object, rights: Tuple[int]):
    api_method.chmod(one_object._id, *rights)
    assert _rights_as_tuple(one_object) == rights



def cant_be_chmod___test(api_method, one_object, rights: Tuple[int]):
    old_rights = _rights_as_tuple(one_object)
    with pytest.raises(OneException):
        api_method.chmod(one_object._id, *rights)
    new_rights = _rights_as_tuple(one_object)
    assert old_rights == new_rights
    