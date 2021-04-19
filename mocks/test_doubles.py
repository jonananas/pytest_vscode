from os import path
from fileio import FileIO


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


class FileIODummy(FileIO):

    def readlines(self, filename: str) -> list[str]:
        return None

    def writelines(self, filename: str, lines: list[str]):
        pass


class FileIOStub(FileIO):

    def readlines(self, filename: str) -> list[str]:
        return ["key=value"]

    def writelines(self, filename: str, lines: list[str]):
        pass


class FileIOSpy(FileIO):

    def __init__(self):
        self.writeCalled = False

    def readlines(self, filename: str) -> list[str]:
        return ["key=value"]

    def writelines(self, filename: str, lines: list[str]):
        self.writeCalled = True


class FileIOFake(FileIO):

    def __init__(self):
        self.fileContents = list()

    def readlines(self, filename: str) -> list[str]:
        return self.fileContents

    def writelines(self, filename: str, lines: list[str]):
        self.fileContents = lines


class TestDoubles:

    def test_that_dotenv_write_is_disabled_using_dummy(self):
        dotEnv = DotEnv(FileIODummy())
        dotEnv.write(".env", {})
        assert not path.exists(".env")

    def test_should_read(self):
        dotEnv = DotEnv(FileIOStub())
        assert dotEnv.read(".env") != None

    def test_should_write(self):
        spy = FileIOSpy()
        dotEnv = DotEnv(spy)
        dotEnv.write(".env", {})
        assert spy.writeCalled

    def test_that_we_can_write_and_read(self):
        dotEnv = DotEnv(FileIOFake())
        dotEnv.write(".env", {"key": "value"})
        env = dotEnv.read(".env")
        assert env['key'] == "value"
