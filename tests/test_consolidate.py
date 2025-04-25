from pathlib import Path

import pytest

from warn_transformer import consolidate

# from urllib3.connection import HTTPSConnection


@pytest.mark.vcr()
def test_consolidate():
    """Test consolidate."""
    this_dir = Path(__file__).parent
    input_dir = this_dir / "data" / "raw"
    consolidate.run(input_dir)
