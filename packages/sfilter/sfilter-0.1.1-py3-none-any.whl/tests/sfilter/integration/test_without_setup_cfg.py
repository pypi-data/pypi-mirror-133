import os

from click.testing import CliRunner

from src.sfilter.cli import main


def test_one_file():
    file_name = "simple.py"
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open(file_name, "w") as f:
            f.write("import os")
            file_path = os.path.realpath(f.name)

        result = runner.invoke(main, [file_path])
        assert result.exception is None
        assert result.exit_code == 0
