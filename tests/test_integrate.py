import pytest

from warn_transformer import integrate


@pytest.mark.vcr()
def test_integrate():
    """Test integrate."""
    integrate.run()
