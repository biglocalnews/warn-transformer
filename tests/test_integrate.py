from pathlib import Path

import pytest

from warn_transformer import integrate


@pytest.mark.runvcr
@pytest.mark.vcr()
def test_integrate():
    """Test integrate."""
    this_dir = Path(__file__).parent
    new_path = this_dir / "data" / "processed" / "consolidated.csv"
    integrate.run(new_path, init_current_data=True)
