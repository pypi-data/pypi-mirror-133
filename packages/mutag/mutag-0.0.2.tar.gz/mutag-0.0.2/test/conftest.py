import pytest

from mutag.train.modules import Conv2DStacked


@pytest.fixture(scope="session")
def conv_2d_stacked():
    return Conv2DStacked(64, 3)
