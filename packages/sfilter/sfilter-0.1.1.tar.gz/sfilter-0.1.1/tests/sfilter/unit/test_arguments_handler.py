from pathlib import Path

from src.sfilter.arguments_handler import parse_arguments


def test_path_without_file():
    test_path = "/etc"
    args = parse_arguments(path=test_path)

    assert args.dir_path == Path(test_path)
    assert args.file_name is None


def test_path_and_file():
    test_path = "/etc/"
    test_file = "file.py"
    args = parse_arguments(path=test_path + test_file)

    assert args.dir_path == Path(test_path)
    assert args.file_name == test_file
