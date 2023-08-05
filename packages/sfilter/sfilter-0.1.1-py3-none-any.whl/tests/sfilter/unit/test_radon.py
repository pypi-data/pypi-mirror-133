import pytest  # noqa

from src.sfilter.file_handling.file_finder import find_file
from src.sfilter.tools.radon import run_radon
from tests.sfilter.unit.fixtures import create_temp_file  # noqa


@pytest.mark.parametrize(
    "create_temp_file",
    [{"file_name": "temp_test_radon.py", "file_content": "import os"}],
    indirect=True,
)
def test_radon(create_temp_file):
    """Test that radon is launched"""
    expected_content = '{"mi": 100.0, "rank": "A"}'
    run_radon(create_temp_file.name())

    file_handler = find_file("radon.json")
    actual_content = file_handler.get_content()
    file_handler.delete()

    assert expected_content in actual_content
