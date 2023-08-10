import pytest


def pytest_addoption(parser):
    """Add an argument to run the download and integrate tests."""
    parser.addoption("--runvcr", action="store_true", default=False, help="run VCR")


def pytest_configure(config):
    """Marker to tell VCR tests to run."""
    config.addinivalue_line("markers", "runvcr: mark test to run vcr")


def pytest_collection_modifyitems(config, items):
    """Ensure tests only run if --runvcr flag is supplied."""
    if config.getoption("--runvcr"):
        # --runvcr given in cli: will run vcr tests
        return
    run_vcr = pytest.mark.skip(reason="need --runvcr option to run")
    for item in items:
        if "runvcr" in item.keywords:
            item.add_marker(run_vcr)


@pytest.fixture(scope="module")
def vcr_config():
    """Replace API token with dummy placeholder."""
    return {"filter_headers": [("authorization", "DUMMY")]}
