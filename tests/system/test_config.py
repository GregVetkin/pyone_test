from api  import One






def test_get_config(one: One):
    config  = one.system.config()
    assert config.has__content() == True

