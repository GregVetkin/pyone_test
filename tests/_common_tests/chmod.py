import pytest
import random
from pyone      import OneNoExistsException




def _rights_as_bool_tuples(one_object):
    rights = one_object.info().PERMISSIONS

    return ((rights.OWNER.USE, rights.OWNER.MANAGE, rights.OWNER.ADMIN),
            (rights.GROUP.USE, rights.GROUP.MANAGE, rights.GROUP.ADMIN),
            (rights.OTHER.USE, rights.OTHER.MANAGE, rights.OTHER.ADMIN))







def test_chmod_if_not_exist(api_method):
    with pytest.raises(OneNoExistsException):
        api_method.chmod(999999)




def test_chmod(api_method, one_object):

    api_method.chmod(one_object._id, user_use=1)
    assert _rights_as_bool_tuples(one_object) == (  (True, False, False), 
                                                    (False, False, False), 
                                                    (False, False, False))

    api_method.chmod(one_object._id, user_manage=1)
    assert _rights_as_bool_tuples(one_object) == (  (True, True, False), 
                                                    (False, False, False), 
                                                    (False, False, False))

    api_method.chmod(one_object._id, user_admin=1)
    assert _rights_as_bool_tuples(one_object) == (  (True, True, True), 
                                                    (False, False, False), 
                                                    (False, False, False))

    api_method.chmod(one_object._id, user_admin=0)
    assert _rights_as_bool_tuples(one_object) == (  (True, True, False), 
                                                    (False, False, False), 
                                                    (False, False, False))

    api_method.chmod(one_object._id, user_manage=0)
    assert _rights_as_bool_tuples(one_object) == (  (True, False, False), 
                                                    (False, False, False), 
                                                    (False, False, False))
    
    api_method.chmod(one_object._id, user_use=0)
    assert _rights_as_bool_tuples(one_object) == (  (False, False, False), 
                                                    (False, False, False), 
                                                    (False, False, False))

    api_method.chmod(one_object._id, group_use=1)
    assert _rights_as_bool_tuples(one_object) == (  (False, False, False), 
                                                    (True, False, False), 
                                                    (False, False, False))

    api_method.chmod(one_object._id, group_manage=1)
    assert _rights_as_bool_tuples(one_object) == (  (False, False, False), 
                                                    (True, True, False), 
                                                    (False, False, False))

    api_method.chmod(one_object._id, group_admin=1)
    assert _rights_as_bool_tuples(one_object) == (  (False, False, False), 
                                                    (True, True, True), 
                                                    (False, False, False))

    api_method.chmod(one_object._id, group_admin=0)
    assert _rights_as_bool_tuples(one_object) == (  (False, False, False), 
                                                    (True, True, False), 
                                                    (False, False, False))

    api_method.chmod(one_object._id, group_manage=0)
    assert _rights_as_bool_tuples(one_object) == (  (False, False, False), 
                                                    (True, False, False), 
                                                    (False, False, False))
    
    api_method.chmod(one_object._id, group_use=0)
    assert _rights_as_bool_tuples(one_object) == (  (False, False, False), 
                                                    (False, False, False), 
                                                    (False, False, False))

    api_method.chmod(one_object._id, other_use=1)
    assert _rights_as_bool_tuples(one_object) == (  (False, False, False), 
                                                    (False, False, False), 
                                                    (True, False, False))

    api_method.chmod(one_object._id, other_manage=1)
    assert _rights_as_bool_tuples(one_object) == (  (False, False, False), 
                                                    (False, False, False), 
                                                    (True, True, False))

    api_method.chmod(one_object._id, other_admin=1)
    assert _rights_as_bool_tuples(one_object) == (  (False, False, False), 
                                                    (False, False, False), 
                                                    (True, True, True))

    api_method.chmod(one_object._id, other_admin=0)
    assert _rights_as_bool_tuples(one_object) == (  (False, False, False), 
                                                    (False, False, False), 
                                                    (True, True, False))

    api_method.chmod(one_object._id, other_manage=0)
    assert _rights_as_bool_tuples(one_object) == (  (False, False, False), 
                                                    (False, False, False), 
                                                    (True, False, False))
    
    api_method.chmod(one_object._id, other_use=0)
    assert _rights_as_bool_tuples(one_object) == (  (False, False, False), 
                                                    (False, False, False), 
                                                    (False, False, False))
