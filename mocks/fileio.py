
class FileIO:
    def readlines(self, filename: str) -> list[str]:
        with open(filename, "r") as file:
            return file.readlines()

    def writelines(self, filename: str, lines: list[str]):
        with open(filename, "w") as file:
            for line in lines:
                file.write(line)
