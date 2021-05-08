from fileio import FileIO
import pytest
import os


class DotEnv:
    def __init__(self, fileIO: FileIO = FileIO()):
        self._fileIO = fileIO

    def read(self, path: str) -> dict:
        res = dict()
        for line in self._fileIO.readlines(path):
            key, value = line.split("=")
            res[key] = value.rstrip()
        return res

    def write(self, path: str, env: dict):
        lines = []
        for key, value in env.items():
            lines.append(f"{key}={value}\n")
        self._fileIO.writelines(path, lines)


class TestDotEnvIntegration:

    def test_that_reads_and_writes(self):
        dotenv = DotEnv()
        env = {"KEY": "VALUE", "KEY2": "VALUE2"}

        dotenv.write(".env", env)
        assert dotenv.read(".env").get("KEY") == "VALUE"
        os.remove(".env")


class TestDotEnv:

    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.fileIO: FileIO = mocker.Mock()
        self.dotenv = DotEnv(self.fileIO)

    def test_that_writes_file(self):
        env = {"KEY": "VALUE", "KEY2": "VALUE2"}
        self.dotenv.write(".env", env)

        assert self.fileIO.writelines.call_args[0][0] == ".env"
        assert self.fileIO.writelines.call_args[0][1] == ["KEY=VALUE\n", "KEY2=VALUE2\n"]

    def test_that_write_exception_propagates(self):
        self.fileIO.writelines.side_effect = Exception("File cannot be written")

        with pytest.raises(Exception):
            self.dotenv.write("bad path", dict())

    def test_that_read_exception_propagates(self):
        self.fileIO.readlines.side_effect = Exception("File not found")

        with pytest.raises(Exception):
            self.dotenv.read("bad file")
        assert self.fileIO.readlines.call_args[0][0] == "bad file"

    def test_that_reads_multiple_lines(self):
        self.fileIO.readlines.return_value = ["KEY=VALUE\n", "KEY2=VALUE2\n"]

        assert list(self.dotenv.read(".env").keys()) == ["KEY", "KEY2"]

    def test_that_read_returns_dict(self):
        self.fileIO.readlines.return_value = ["KEY=VALUE\n"]

        assert self.dotenv.read(".env").get("KEY") == "VALUE"

    def test_that_DotEnv_takes_FileIO(self):
        assert self.dotenv._fileIO == self.fileIO

    def test_that_DotEnv_defaults_to_FileIO(self):
        dotenv = DotEnv()
        assert type(dotenv._fileIO) == FileIO
