import os
import string

# *File Info
__author__ = "Reuben Taylor"
__version__ = "v1.1.0-alpha"


def main():
    """Main entry point of the app"""
    # mode = input("################\n## Please select a mode. ##\n1 - Search\n2 - Compression\nDecompression")
    mode = 2
    match mode:
        case 1:
            searchMenu()
        case 2:
            compressionMenu()
        # case 3:
        #     decompressionMenu()


def compressionMenu():
    """Menu for compressing text"""
    brokenTextWithoutPunctuation = getSelectedFileText()
    # typeOfCompression = input("################\n## Please select a type of compression. ##\n1 - Level 1 Compression\n2 - Level 2 Compression")
    # fileName = input("Enter a file name to save the compressed text to.")
    typeOfCompression = 1
    fileName = "output"
    match typeOfCompression:
        case 1:
            level1Compression(
                brokenTextWithoutPunctuation,
                turnSelectedFileToPath(fileName, "output files"),
            )


def searchMenu():
    """Menu for searching text"""
    brokenTextWithoutPunctuation = getSelectedFileText()
    typeOfSearch = input(
        "################\n## Please select a type of search. ##\n1 - Find the position(s) of a word in the text file."
    )
    match typeOfSearch:
        case 1:
            printableWordIndicies = returnIndiciesOfWordInText(
                brokenTextWithoutPunctuation
            )
            print(f"Word was found at following positions:\n{printableWordIndicies}")


def getSelectedFileText():
    """Gets text from the selected file"""
    # selectedFile = input("Please enter the name of a text file to read from. Do not include a file extention.")
    selectedFile = "sentence"
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
    # wordToLookFor = input("Please enter the word you wish to search for in the file.")
    wordToLookFor = "Ask"
    wordIndicies = findWord(wordToLookFor, text)
    printableWordIndicies = makeWordIndiciesPrintable(wordIndicies)
    return printableWordIndicies


def level1Compression(text, fileName):
    """Compresses text to list of values that can be accessed in a hashmap"""
    wordHashmap = makeHashmapOfWords(text)
    compressedText = convertTextToWordHashmapValues(text, wordHashmap)
    saveCompressedTextToFile(compressedText, wordHashmap, fileName)


def saveCompressedTextToFile(compressedText, wordHashmap, fileName):
    try:
        with open(fileName, "w") as f:
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
