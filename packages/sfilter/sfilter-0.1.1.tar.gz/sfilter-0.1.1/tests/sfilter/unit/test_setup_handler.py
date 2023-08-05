import pytest

from src.sfilter.file_handling.file_finder import find_file
from src.sfilter.setup_handler import SetUpHandler
from tests.sfilter.unit.fixtures import roll_back_file  # noqa


def test_sfilter_section_is_present():
    assert SetUpHandler().has_section("sfilter")


@pytest.mark.parametrize("roll_back_file", ["setup.cfg"], indirect=True)
def test_setup_writes_without_changes(roll_back_file):
    content_before = _setup_file_content()
    SetUpHandler().save()
    content_after = _setup_file_content()
    assert content_before == content_after


@pytest.mark.parametrize("roll_back_file", ["setup.cfg"], indirect=True)
def test_flake8_value_can_be_updated(roll_back_file):
    content_before = _setup_file_content()
    setup_h = SetUpHandler()

    flake8_init_value = setup_h.get("flake8")
    flake8_temp_value = str(int(flake8_init_value) + 1)
    setup_h.set("flake8", flake8_temp_value)
    setup_h.save()

    content_after = _setup_file_content()
    assert content_before != content_after


def _setup_file_content():
    return find_file("setup.cfg").get_content()
