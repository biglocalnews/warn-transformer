import tempfile
from pathlib import Path

import pytest

from warn_transformer import download

# from urllib3.connection import HTTPSConnection


@pytest.mark.runvcr
@pytest.mark.vcr()
def test_download():
    """Test download."""
    download.run(Path(tempfile.gettempdir()))
