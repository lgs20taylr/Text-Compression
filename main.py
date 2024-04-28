import os
import re
import string

# *File Info
__author__ = "Reuben Taylor"
__version__ = "v1.1.0-alpha"


def main():
    """Main entry point of the app"""
    mode = int(
        input(
            "\n## Please select a mode. ##\n1 - Search\n2 - Compression\n3 - Decompression\n"
        )
    )
    match mode:
        case 1:
            searchMenu()
        case 2:
            print("a")
            compressionMenu()
        case 3:
            decompressionMenu()


def searchMenu():
    """Menu for searching text"""
    brokenTextWithoutPunctuation = getSelectedFileText()
    typeOfSearch = int(
        input(
            "\n## Please select a type of search. ##\n1 - Find the position(s) of a word in the text file.\n"
        )
    )
    match typeOfSearch:
        case 1:
            printableWordIndicies = returnIndiciesOfWordInText(
                brokenTextWithoutPunctuation
            )
            print(f"Word was found at following positions:\n{printableWordIndicies}")


def compressionMenu():
    """Menu for compressing text"""
    brokenTextWithoutPunctuation = getSelectedFileText()
    typeOfCompression = int(
        input(
            "\n## Please select a type of compression. ##\n1 - Level 1 Compression\n2 - Level 2 Compression\n"
        )
    )
    outputFileName = input(
        "Enter a file name to save the compressed text to. Do not include a file extension.\n"
    )
    outputFilePath = turnSelectedFileToPath(outputFileName, "output files")
    match typeOfCompression:
        case 1:
            level1Compression(brokenTextWithoutPunctuation, outputFilePath)


def decompressionMenu():
    """Menu for decompressing text"""
    typeOfCompression = int(
        input(
            "\n## Please select a type of compression to decompress. ##\n1 - Level 1 Compression\n2 - Level 2 Compression\n"
        )
    )
    inputFileName = input(
        "Enter a file name to read the compressed text from. Do not include a file extension.\n"
    )
    inputFilePath = turnSelectedFileToPath(inputFileName)
    outputFileName = input(
        "Enter a file name to save the decompressed text to. Do not include a file extension.\n"
    )
    outputFilePath = turnSelectedFileToPath(outputFileName, "output files")
    match typeOfCompression:
        case 1:
            level1Decompression(inputFilePath, outputFilePath)


def getSelectedFileText():
    """Gets text from the selected file"""
    selectedFile = input(
        "Please enter the name of a text file to read from. Do not include a file extention.\n"
    )
    filePath = turnSelectedFileToPath(selectedFile)
    fileText = getStringFromFile(filePath)
    fileTextWithoutPunctuation = removePunctuation(fileText)
    brokenTextWithoutPunctuation = breakToWords(fileTextWithoutPunctuation)
    return brokenTextWithoutPunctuation


def turnSelectedFileToPath(fileName, directory="input files", fileExtention="txt"):
    """Converts filename into relative path"""
    path = os.path.join(directory, fileName + "." + fileExtention)
    return path


def getStringFromFile(fileToGrabFrom):
    """Converts file into a string containing the text"""
    with open(fileToGrabFrom) as file:
        fileAsString = file.read()
        return fileAsString


def breakToWords(textToBreak):
    """Breaks a string into induvidual words"""
    brokenText = textToBreak.split(" ")
    return brokenText


def removePunctuation(textContainingPunctuation):
    """Removes punctuation from string"""
    textWithoutPunctuation = textContainingPunctuation.translate(
        str.maketrans("", "", string.punctuation)
    )
    return textWithoutPunctuation


def findWord(word, brokenText):
    """Find indicies of word in text"""
    word = word.upper()
    wordIndices = [i for i, x in enumerate(brokenText) if x == word]
    return wordIndices


def makeWordIndiciesPrintable(wordIndicies):
    """Makes the list of word indicies as a printable string with each index separated by commas"""
    printableWordIndicies = ""
    for index in range(len(wordIndicies)):
        printableWordIndicies = printableWordIndicies + str(wordIndicies[index]) + ", "
    printableWordIndicies = printableWordIndicies.rstrip(", ")
    return printableWordIndicies


def returnIndiciesOfWordInText(text):
    wordToLookFor = input("Please enter the word you wish to search for in the file.\n")
    wordIndicies = findWord(wordToLookFor, text)
    printableWordIndicies = makeWordIndiciesPrintable(wordIndicies)
    return printableWordIndicies


def level1Compression(text, fileName):
    """Compresses text to list of values that can be accessed in a hashmap"""
    wordHashmap = makeHashmapOfWords(text)
    compressedText = convertTextToWordHashmapValues(text, wordHashmap)
    saveCompressedTextToFile(compressedText, wordHashmap, fileName)


def level1Decompression(inputFilePath, outputFilePath):
    with open(inputFilePath) as file:
        compressedTextString = file.readline()[1:-1]
        wordHashmapString = file.readline()[1:-1]
    compressedText = compressedTextString.split(", ")
    wordHashmap = stringToHashmap(wordHashmapString)
    decompressedText = convertWordHashmapValuesToText(compressedText, wordHashmap)
    saveDecompressedTextToFile(
        decompressedText, compressedText, wordHashmap, outputFilePath
    )


def stringToHashmap(stringToConvert):
    hashmap = {}
    stringToConvertList = stringToConvert.split(", ")
    for i in stringToConvertList:
        word = re.findall("'.*'", i)[0][1:-1]
        position = re.findall(": .*", i)[0][2:]
        if position[-1] == "}":
            position = position[:-1]
        hashmap[word] = position
    return hashmap


def saveCompressedTextToFile(compressedText, wordHashmap, outputFilePath):
    try:
        with open(outputFilePath, "w") as f:
            f.write(str(compressedText))
            f.write("\n")
            f.write(str(wordHashmap))
        print("File saved successfully!")
    except Exception as e:
        print(f"File save unsuccessful.\n{e}")


def saveDecompressedTextToFile(
    decompressedText, compressedText, wordHashmap, outputFilePath
):
    try:
        with open(outputFilePath, "w") as f:
            f.write(str(decompressedText))
            f.write("\n")
            f.write(str(compressedText))
            f.write("\n")
            f.write(str(wordHashmap))
        print("File saved successfully!")
    except Exception as e:
        print(f"File save unsuccessful.\n{e}")


def makeHashmapOfWords(text):
    """Creates a hashmap containing each word in a list only once"""
    wordHashmap = {}
    enumeratedText = tuple(enumerate(text))
    hashmapKey = 0
    for _, word in enumeratedText:
        if word not in wordHashmap:
            wordHashmap[word] = hashmapKey
            hashmapKey += 1
    return wordHashmap


def convertTextToWordHashmapValues(text, wordHashmap):
    """Converts each word in a split string to the corresponding hashmap value"""
    compressedText = []
    for word in text:
        wordHashmapValue = wordHashmap[word]
        compressedText.append(wordHashmapValue)
    return compressedText


def convertWordHashmapValuesToText(compressedText, wordHashmap):
    """Converts each value in a list of hashmap keys to the corresponding hashmap value (word)"""
    uncompressedText = []
    for compressedWord in compressedText:
        uncompressedWord = wordHashmap[compressedWord]
        uncompressedText.append(uncompressedWord)
    return uncompressedText


if __name__ == "__main__":
    """Executed when run from commandline"""
    main()
