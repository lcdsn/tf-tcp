from midiutil import MIDIFile


class File:
    def __init__(self, fileName: str, fileContent: str | None = None):
        self.fileName = fileName
        if fileContent:
            self.fileContent = fileContent
        else:
            self.fileContent = None

    def readFile(self):
        try:
            with open(self.fileName, "r") as file:
                self.fileContent = file.read()
        except FileNotFoundError:
            self.fileContent = None

    def saveMIDIFile(self):
        if type(self.fileContent) == MIDIFile:
            with open(self.fileName, "wb") as file:
                self.fileContent.writeFile(file)
        else:
            print("File content is not a MIDIFile object")
