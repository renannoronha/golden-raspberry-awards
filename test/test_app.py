def test_app_is_created(application):
    assert application.name == "src.api"


def test_debug_is_false(config):
    assert config["DEBUG"] is False


def test_testing_is_true(config):
    assert config["TESTING"] is True
