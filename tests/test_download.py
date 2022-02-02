import pytest

from warn_analysis import download


@pytest.mark.vcr()
def test_download():
    """Test download."""
    download.run()
