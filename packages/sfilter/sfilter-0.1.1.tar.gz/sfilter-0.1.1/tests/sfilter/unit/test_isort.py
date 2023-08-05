import pytest  # noqa

from src.sfilter.tools.isort import run_isort
from tests.sfilter.unit.fixtures import create_temp_file  # noqa


@pytest.mark.parametrize(
    "create_temp_file",
    [{"file_name": "temp_test_isort.py", "file_content": "import pathlib\nimport os"}],
    indirect=True,
)
def test_isort(create_temp_file):
    """Test that isort is launched"""
    expected = "import os\nimport pathlib\n"

    run_isort(create_temp_file.name())
    actual = create_temp_file.get_content()

    assert actual == expected
