import pytest
from api        import One
from config     import ADMIN_NAME






@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_get_config(one: One):
    config  = one.system.config()
    assert config.has__content() == True
