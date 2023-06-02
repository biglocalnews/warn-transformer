import pytest


@pytest.fixture(scope='module')
def vcr_config():
    """Replaces API token with dummy placeholder"""
    return {"filter_headers": [('authorization', 'DUMMY')]}
