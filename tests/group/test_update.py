import pytest

from api             import One

from tests._common_methods.update import update_and_merge__test
from tests._common_methods.update import update_and_replace__test
from tests._common_methods.update import update_if_not_exist__test





# =================================================================================================
# TESTS
# =================================================================================================



def test_group_not_exist(one: One):
    update_if_not_exist__test(one.host)


def test_update_by_replace(one: One, dummy_group: int):
    group_id = dummy_group
    update_and_replace__test(one.group, group_id)


def test_update_by_merge(one: One, dummy_group: int):
    group_id = dummy_group
    update_and_merge__test(one.group, group_id)

