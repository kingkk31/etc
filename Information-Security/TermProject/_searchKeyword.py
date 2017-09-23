import logging
import sys

#log file
log = logging.getLogger('main._searchKeyword')

MIN_WORD = 5
MAX_WORD = 15
MAX_PHRASE = 80

PREDECESSOR_SIZE = 80
WINDOW_SIZE = 160

SPACE = ' '

#set target file , keyword file
def ParseCommandLine(inputFile, inputWords):
    global target
    global words
    target = inputFile
    words = inputWords
    return


#search keyword
def SearchWords():

    searchWords = set() #set of keyWords
    searchPhrases = set() #set of keyPhrases
    page = "" #output of result

    #open keyword file and add keywords
    try:
        fileWords = open(words)
        for line in fileWords:
            searchWords.add(line.strip())
    except:
        log.error('Keyword File Failure: ' + words)
        sys.exit()
    finally:
        fileWords.close()


    # open keyphrase file and add keyphrases
    try:
        filePhrase = open(words)
        for line in filePhrase:
            searchPhrases.add(line.strip())
    except:
        log.error('Phrase File Failure: ' + words)
        sys.exit()
    finally:
        filePhrase.close()

    log.info('Search Words')
    log.info('Input File: ' + words)
    log.info(searchWords)

    log.info('Search Phrases')
    log.info('Input File: ' + words)
    log.info(searchPhrases)

    #open target file and put contents of file into bytearray
    try:
        targetFile = open(target, 'rb')
        baTarget = bytearray(targetFile.read())
    except:
        log.error('Target File Failure: ' + target)
        sys.exit()
    finally:
        targetFile.close()

    sizeOfTarget = len(baTarget)

    log.info('Target of Search: ' + target)
    log.info('File Size: ' + str(sizeOfTarget))

    baTargetCopy = baTarget

    #filtering of nonAlphabet
    for i in range(0, sizeOfTarget):
        character = chr(baTarget[i])
        if not character.isalpha() and character != SPACE:
            baTarget[i] = 0

    #words which found
    indexOfWords = []

    cnt = 0
    for i in range(0, sizeOfTarget):
        character = chr(baTarget[i])
        if character.isalpha() or character == SPACE:
            cnt += 1
        else:
            #make phrase
            if (cnt >= MIN_WORD and cnt <= MAX_PHRASE):
                newPhrase = ""
                for z in range(i - cnt, i):
                    newPhrase = newPhrase + chr(baTarget[z])

                newPhrase = newPhrase.lower()

                for eachPhrase in searchPhrases:
                    if eachPhrase in newPhrase:
                        #append result of phrase
                        page += PrintBuffer(newPhrase, i - cnt, baTargetCopy, i - PREDECESSOR_SIZE, WINDOW_SIZE) + "\n"
                        cnt = 0
                        print

                #split phrase and make word
                splitWordList = newPhrase.split()

                for eachWord in splitWordList:
                    if (eachWord in searchWords):
                        #append result of word
                        page += PrintBuffer(eachWord, i - cnt, baTargetCopy, i - PREDECESSOR_SIZE, WINDOW_SIZE) + "\n"
                        #append index of word
                        indexOfWords.append([eachWord, i - cnt])
                        cnt = 0
                        print
                    else:
                        cnt = 0
            else:
                cnt = 0

    #append all words which found
    page += PrintAllWordsFound(indexOfWords)

    #return result
    return page


#head of output
def PrintHeading():
    page = ""
    page += "Offset        00  01  02  03  04  05  06  07  08  09  0A  0B  0C  0D  0E  0F         ASCII\n"
    page += "------------------------------------------------------------------------------------------------\n"
    return page


#output of result
def PrintBuffer(word, directOffset, buff, offset, hexSize):

    page = ""

    page += "Found: " + word + " At Address:  "
    page += ("%08x     \n" % (directOffset))

    page += PrintHeading()

    for i in range(offset, offset + hexSize, 16):
        for j in range(0, 17):
            #start offset
            if (j == 0):
                page += ("%08x      " % i)
            else:
                #other offset
                if i + j >= len(buff):
                    byteValue = ord(' ')
                else :
                    byteValue = buff[i + j]

                page += ("%02x  " % byteValue)
        page += "       "

        #print charactor of offset
        for j in range(0, 16):
            if i + j >= len(buff):
                byteValue = ord(' ')
            else:
                byteValue = buff[i + j]

            if (byteValue >= 0x20 and byteValue <= 0x7f):
                page += ("%c " % byteValue)
            else:
                page += '. '
        page += "\n"

    #return result
    return page


#output of all words
def PrintAllWordsFound(wordList):
    page = ""
    page += "Index of All Words\n"
    page += "---------------------\n"

    wordList.sort()

    for entry in wordList:
        page += str(entry)+'\n'

    page += "---------------------\n\n"

    return page