import random


def __get_random_rights():
    return [random.randint(-1, 1) for _ in range(9)]


def __permissions_class_to_rights_list(permissions_class):
        return [
            permissions_class.OWNER_U, permissions_class.OWNER_M, permissions_class.OWNER_A,
            permissions_class.GROUP_U, permissions_class.GROUP_M, permissions_class.GROUP_A,
            permissions_class.OTHER_U, permissions_class.OTHER_M, permissions_class.OTHER_A,
        ]


def __permissions_changed_correctly(old_permissions, new_permissions, established_rights):
    old_rights_list = __permissions_class_to_rights_list(old_permissions)
    new_rights_list = __permissions_class_to_rights_list(new_permissions)

    for i, value in enumerate(established_rights):
        if value < 0 and old_rights_list[i] != new_rights_list[i]:
            return False

        if value > 0 and new_rights_list[i] != value:
            return False
        
    return True
              





def random_permissions__test(api_object, one_object_id):
    old_permissions = api_object.info(one_object_id).PERMISSIONS
    right_to_set    = __get_random_rights()

    _id = api_object.chmod(one_object_id, *right_to_set)
    assert _id == one_object_id

    new_permissions = api_object.info(one_object_id).PERMISSIONS

    assert __permissions_changed_correctly(old_permissions, new_permissions, right_to_set)
