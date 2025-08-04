from api    import One






def test_raft_status(one: One):
    raft_status = one.zone.raftstatus()
    assert raft_status.has__content()



