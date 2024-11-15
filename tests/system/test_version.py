import pytest
from api        import One
from config     import ADMIN_NAME






@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_get_version(one: One):
    version = one.system.version()
    assert isinstance(version, str), "Полученный объект не является строкой"

