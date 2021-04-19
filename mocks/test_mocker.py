from fileio import FileIO
from os import path


class DotEnv:
    def __init__(self, fileIO=FileIO()):
        self.fileio: FileIO = fileIO

    def read(self, filename: str) -> dict:
        res = dict()
        for line in self.fileio.readlines(filename):
            key, value = line.split("=")
            res[key] = value[:-1]
        return res

    def write(self, filename: str, envdict):
        lines = list()
        for key, value in envdict.items():
            lines.append(f"{key}={value}\n")
        self.fileio.writelines(filename, lines)


class TestDotEnv():

    def test_that_dotenv_write_is_disabled_using_dummy(self, mocker):
        dotEnv = DotEnv(mocker.Mock())
        dotEnv.write(".env", {})
        assert not path.exists(".env")

    def test_should_read(self, mocker):
        mock = mocker.Mock()
        dotEnv = DotEnv(mock)

        mock.readlines.return_value = ["KEY=VALUE"]

        assert dotEnv.read(".env") is not None

    def test_should_write(self, mocker):
        mock = mocker.Mock()
        dotEnv = DotEnv(mock)

        dotEnv.write(".env", {})

        assert mock.writelines.called

    def test_that_we_can_write_and_read(self, mocker):
        mock = mocker.Mock()
        dotEnv = DotEnv(mock)
        self.file_contents = list()

        def side_effect_writelines(filename: str, lines: list[str]):
            self.file_contents = lines

        def side_effect_readlines(filename: str) -> list[str]:
            return self.file_contents

        dotEnv.fileio.writelines.side_effect = side_effect_writelines
        dotEnv.fileio.readlines.side_effect = side_effect_readlines

        dotEnv.write(".env", {"key": "value"})

        env = dotEnv.read(".env")
        assert env['key'] == "value"

    def test_that_write_lines(self, mocker):
        mock = mocker.Mock()
        dotEnv = DotEnv(mock)

        dotEnv.write(".env", {"key": "value"})

        assert mock.writelines.call_args.args[1] == ["key=value\n"]
