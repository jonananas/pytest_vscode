from os import path, remove
from fileio import FileIO


# Integration tests:
class TestFileIO:

    def test_readlines(self):
        filename = "kasta.env"
        assert not path.exists(filename)
        contents = ["one\n", "two three\n"]
        FileIO().writelines(filename, contents)

        assert FileIO().readlines(filename) == contents

        remove(filename)
        assert not path.exists(filename)

    def test_writelines(self):
        filename = "kasta.env"
        assert not path.exists(filename)

        lines = ["first\n", "Second\n"]
        FileIO().writelines(filename, lines)
        assert path.exists(filename)
        assert FileIO().readlines(filename) == lines

        remove(filename)
        assert not path.exists(filename)
