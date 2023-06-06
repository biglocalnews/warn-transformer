import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--runvcr", action="store_true", default=False, help="run VCR"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "runvcr: mark test to run vcr")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runvcr"):
        # --runvcr given in cli: will run vcr tests
        return
    run_vcr = pytest.mark.skip(reason="need --runvcr option to run")
    for item in items:
        if "runvcr" in item.keywords:
            item.add_marker(run_vcr)

@pytest.fixture(scope='module')
def vcr_config():
    """Replace API token with dummy placeholder."""
    return {"filter_headers": [('authorization', 'DUMMY')]}
