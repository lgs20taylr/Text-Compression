import os

# *File Info
__author__ = "Reuben Taylor"
__version__ = "v0.0.0-alpha"


def main():
    """Main entry point of the app"""
    # selectedFile = input("Please enter the name of a text file to read from (without extention).")
    selectedFile = "sentence"
    print(breakToWords(getStringFromFile(turnSelectedFileToPath(selectedFile, "txt"))))


def turnSelectedFileToPath(fileName, fileExtention):
    path = os.path.join("text files", fileName + "." + fileExtention)
    return path


def getStringFromFile(fileToGrabFrom):
    with open(fileToGrabFrom) as file:
        fileAsString = file.read()
        return fileAsString


def breakToWords(textToBreak):
    brokenText = textToBreak.split(" ")
    return brokenText


if __name__ == "__main__":
    """Executed when run from commandline"""
    main()
