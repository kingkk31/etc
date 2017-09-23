import os
import time
import hashlib
import csv
import logging

#log file
log = logging.getLogger('main._hashDir')

#set directory, hash mode
def ParseCommandLine(str1, str2):

    global gl_args
    global gl_hashType

    gl_args = str1

    if str2 == "MD5":
        gl_hashType = 'MD5'
    elif str2 == "SHA1":
        gl_hashType = 'SHA1'
    elif str2 == "SHA256":
        gl_hashType = 'SHA256'
    elif str2 == "SHA384":
        gl_hashType = 'SHA384'
    elif str2 == "SHA512":
        gl_hashType = 'SHA512'
    else:
        gl_hashType = "Unknown"
        logging.error('Unknown Hash Type Specified')

    return


#walk path of directory and start hashing
def WalkPath():

    processCount = 0
    errorCount = 0

    log.info('Root Path: ' + gl_args + "\n")

    #list of result
    resultList = []

    #get file in directory and hash file
    for root, dirs, files in os.walk(gl_args):
        for file in files:

            fname = os.path.join(root, file)
            resultHash = HashFile(fname, file, gl_hashType) #start hashing and store result

            #append result to list
            if resultHash :
                resultList.append(resultHash)
                processCount += 1
            else:
                errorCount += 1

    return (processCount, resultList)


#hash directory
def HashFile(theFile, simpleName, hashType):

    if os.path.exists(theFile):
        if not os.path.islink(theFile):
            if os.path.isfile(theFile):

                #open file
                try:
                    f = open(theFile, 'rb')
                except IOError:
                    log.warning('Open Failed: ' + theFile)
                    return
                else:
                    #read file
                    try:
                        rd = f.read()
                    except IOError:
                        f.close()
                        log.warning('Read Failed: ' + theFile)
                        return
                    else:
                        #get stats of file
                        theFileStats = os.stat(theFile)
                        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(theFile)

                        fileSize = str(size)

                        modifiedTime = time.ctime(mtime)
                        accessTime = time.ctime(atime)
                        createdTime = time.ctime(ctime)

                        ownerID = str(uid)
                        groupID = str(gid)
                        fileMode = bin(mode)

                        #make hash value about hash mode selected
                        if gl_hashType == "MD5":
                            hash = hashlib.md5()
                            hash.update(rd)
                            hexMD5 = hash.hexdigest()
                            hashValue = hexMD5.upper()
                        elif gl_hashType == "SHA1":
                            hash = hashlib.sha1()
                            hash.update(rd)
                            hexSHA1 = hash.hexdigest()
                            hashValue = hexSHA1.upper()
                        elif gl_hashType == "SHA256":
                            hash = hashlib.sha256()
                            hash.update(rd)
                            hexSHA256 = hash.hexdigest()
                            hashValue = hexSHA256.upper()
                        elif gl_hashType == "SHA384":
                            hash = hashlib.sha384()
                            hash.update(rd)
                            hexSHA384 = hash.hexdigest()
                            hashValue = hexSHA384.upper()
                        elif gl_hashType == "SHA512":
                            hash = hashlib.sha512()
                            hash.update(rd)
                            hexSHA512 = hash.hexdigest()
                            hashValue = hexSHA512.upper()
                        else:
                            log.error('Hash not Selected')
                        f.close()

                        #temporary list of result
                        resultArr = []
                        resultArr.append(simpleName)
                        resultArr.append(theFile)
                        resultArr.append(fileSize)
                        resultArr.append(modifiedTime)
                        resultArr.append(accessTime)
                        resultArr.append(createdTime)
                        resultArr.append(hashType)
                        resultArr.append(hashValue)
                        resultArr.append(ownerID)
                        resultArr.append(groupID)
                        resultArr.append(mode)

                        log.info("+-------------------------------------------------------------")
                        log.info("+File Path:  " + theFile)
                        log.info("+File Name:  " + simpleName)
                        log.info("+Hash Type:  " + gl_hashType)
                        log.info("+Hash Value: " + hashValue)
                        log.info("+-------------------------------------------------------------\n")

                        #return result list
                        return resultArr
            else:
                log.warning('[' + repr(simpleName) + ', Skipped NOT a File' + ']')
                return False
        else:
            log.warning('[' + repr(simpleName) + ', Skipped Link NOT a File' + ']')
            return False
    else:
        log.warning('[' + repr(simpleName) + ', Path does NOT exist' + ']')
    return False


#CSV file class
class _CSVWriter:
    def __init__(self, fileName, hashType):
        try:
            self.csvFile = open(fileName, 'wb')
            self.writer = csv.writer(self.csvFile, delimiter=',', quoting=csv.QUOTE_ALL)
            self.writer.writerow(('File', 'Path', 'Size', 'Modified Time', 'Access Time', 'Created Time', hashType,
                                  'Owner', 'Group', 'Mode'))
        except:
            log.error('CSV File Failure')

    #write row
    def writeCSVRow(self, fileName, filePath, fileSize, mTime, aTime, cTime, hashVal, own, grp, mod):
        self.writer.writerow((fileName, filePath, fileSize, mTime, aTime, cTime, hashVal, own, grp, mod))

    def writerClose(self):
        self.csvFile.close()
