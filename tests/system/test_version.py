from api   import One





def test_get_version(one: One):
    version = one.system.version()
    assert isinstance(version, str), "Полученный объект не является строкой"
