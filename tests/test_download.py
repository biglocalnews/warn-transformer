import tempfile
from pathlib import Path

import pytest

from warn_transformer import download


@pytest.mark.vcr()
def test_download():
    """Test download."""
    download.run(Path(tempfile.gettempdir()))
