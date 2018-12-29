//Author Alexander Kessaris

import re
import sys

#Run the following command: python ank352_HW5_test.py ../WSJ_CHUNK_FILES/WSJ_24.pos

#Take pos-chunk file as input
file = open(sys.argv[1], "r")

#Create iterable version of file to retrieve next lines
fileCopy = open(sys.argv[1], "r")
fileIter = iter(fileCopy)
next(fileIter)

#Test feature file
testFile = open("test.feature", "w+")

#Separator for values (tabs in this case)
sep = "\t"

#Punctuation
punct = re.compile("[a-zA-Z0-9\-&]")

#Name dictionary
nameDict = ["Mr.", "Mister", "Mrs.", "Ms.", "Dr.", "Doctor", "Professor", "Prof", "Sir"]

#Organization dictionary
orgDict = ["Inc.", "Co.", "Incorporated"]

def main():
    #Make feature value pairs
    makePairs(file)

#Makes feature value pairs from input file
def makePairs(file):
    #Previous feature value pairs in file
    prevFeatArr = []
    for i in range(3):
        prevFeatArr.append(createFeat())
    
    #Next feature value pairs in file
    nextFeatArr = []
    for i in range(2):
        nextFeatArr.append(getFeat(next(fileIter)))

    testOutput = "" #Output to test file
    
    #Iterate through file
    for line in file:
        #If blank line in file, write blank line to file
        if (line == "\n"):
            #Set previous feature value pairs
            for feat in prevFeatArr:
                feat = createFeat()
            
            #Add blank lines to testing output
            testOutput += "\n"
            
            #Go to next line
            continue
        
        #Get feature value pairs for next lines
        nextIndex = 0
        while (nextIndex < (len(nextFeatArr)-1)):
            nextFeatArr[nextIndex] = nextFeatArr[nextIndex+1]
            nextIndex += 1
        nextFeatArr[len(nextFeatArr)-1] = getFeat(next(fileIter))

        #Get values for current line
        currFeat = getFeat(line)

        #Check if any of the feature pairs contain names
#        featArr = isName(prevFeatArr, currFeat, nextFeatArr)
#        prevFeatArr = featArr[0]
#        currFeat = featArr[1]
#        nextFeatArr = featArr[2]

#        orgArray = isOrg(prevFeatArr, currFeat, nextFeatArr)
#        prevFeatArr = orgArray[0]
#        currFeat = orgArray[1]
#        nextFeatArr = orgArray[2]

        #Add current feature value pairs to output
        testOutput += currFeat["word"] + sep + "POS=" + currFeat["pos"] + sep + "cap=" + currFeat["cap"]
        
        #If not at beginning of sentence, add features of previous words
        for index, feat in enumerate(prevFeatArr):
            if (feat["word"] != ""):
                testOutput += featToString("prev", str(index+1), feat)
        
        #If not at end of sentence, add steps features of next words
        for index, feat in enumerate(nextFeatArr):
            if (feat["word"] != ""):
                testOutput += featToString("next", str(index+1), feat)
    
        #Add new lines to output
        testOutput += "\n"

        #Set previous feature values
        i = len(prevFeatArr)-1
        while i > 0:
            prevFeatArr[i] = prevFeatArr[i-1]
            i -= 1
        prevFeatArr[0] = currFeat
    
    #Write feature value pairs to test file
    testFile.write(testOutput)

#Takes line as argument returns array with word, pos, and bio features
def getFeat(line):
    arr = createFeat()
    
    #If line is blank, return blank tags
    if (line == "\n"):
        return arr
    
    #Split the line up by tabs
    splitLine = line.split("\t")
    
    #Extract current bio and word
    arr["word"] = splitLine[0]

    #Check if word is part of name
#    if (arr["word"] in nameDict):
#        arr["name"] = "true"
#
#    #Check if word is part of organization
#    if (arr["word"] in orgDict):
#        arr["org"] = "true"

    # If token represents punctuation, set current POS to PU
    if (not punct.match(line)):
        arr["pos"] = "PU"
    #Otherwise, extract it normally from line
    else:
        arr["pos"] = splitLine[1].replace('\n', '')

    #Check capitalization
    if (arr["word"][0].isupper()):
        arr["cap"] = "true"
    
    #Return array
    return arr

#Returns dictionary of feature value pairs
def createFeat():
    return {"word": "", "pos": "", "cap": "false"}

#Takes string (previous, current, next), which one it is (1, 2, 3, etc), and the feature pair dictionary and returns string to add to output file
def featToString(str, num, feat):
    output = ""
    for key in feat:
        output += sep + str + "_" + key + "_" + num + "=" + feat[key]
    return output

#Takes previous, current, and next feature arrays and determines which elements are names (returns updated versions of feature arrays)
# Pass in previous, current, and next feature array
def isName(prevFeatArr, currFeat, nextFeatArr):
    #Look through previous features to find cases of names
    for index, feat in (enumerate(prevFeatArr)):
        #Prevent index out of bounds error
        if (index > 0):
            #If current word is in nameDict or is part of a name, set previous name to true
            if (feat["word"] in nameDict or (feat["name"] == "true" and prevFeatArr[index-1]["cap"]=="true")):
                prevFeatArr[index-1]["name"] = "true"

    #Check current word
    if prevFeatArr[0]["word"] in nameDict:
        currFeat["name"] = "true"
        
    if currFeat["word"] in nameDict:
        currFeat["name"] = "true"
        if (nextFeatArr[0]["cap"] == "true"):
            nextFeatArr[0]["name"] = "true"

    #If word is capitilized, but not at beginning of sentence, make it a name
    if (currFeat["cap"] == "true" and prevFeatArr[0]["word"] != ""):
        currFeat["name"] = "true"

    #Check next words
    for index, feat in enumerate(nextFeatArr):
        #Prevent index out of bounds error
        if (index < (len(nextFeatArr)-1)):
            #If current word is in nameDict or is part of a name, set name to true
            if (feat["word"] in nameDict or (feat["name"] == "true" and nextFeatArr[index+1]["cap"]=="true")):
                nextFeatArr[index+1]["name"] = "true"

    if (currFeat["cap"] == "true" and nextFeatArr[0]["name"] == "true"):
        currFeat["name"] = "true"

    #Return array holding updated feature arrays
    return [prevFeatArr, currFeat, nextFeatArr]

#Takes previous, current, and next feature arrays and determines which elements are names (returns updated versions of feature arrays)
# Pass in previous, current, and next feature array
def isOrg(prevFeatArr, currFeat, nextFeatArr):
    #Check next future arrays
    for index, feat in enumerate(nextFeatArr):
        #If current word is in organization dictionary, set org to true
        if nextFeatArr[index]["word"] in orgDict:
            nextFeatArr[index]["org"] = "true"
            #Check if any previous words are also part of the organization
            i = index-1
            while (i >= 0 and nextFeatArr[i]["cap"] == "true"):
                nextFeatArr[i]["org"] = "true"
                i -= 1

    #Check current word
    if (nextFeatArr[0]["org"] == "true" and currFeat["cap"] == "true"):
        currFeat["org"] = "true"
        
    #See if previous word is also part of organization
    if (currFeat["org"] == "true" and prevFeatArr[0]["cap"] == "true"):
        prevFeatArr[0]["org"] = "true"
        
    #Check previous feature arrays
    if (currFeat["org"] == "true"):
        if (prevFeatArr[0]["cap"] == "true"):
            prevFeatArr[0]["org"] = "true"
    for index, feat in enumerate(prevFeatArr):
        #If current word is in organization dictionary, set org to true
        if prevFeatArr[index]["word"] in orgDict:
            prevFeatArr[index]["org"] = "true"
            #Check previous words to see if also an organization
            i = index+1
            while (i < len(prevFeatArr) and prevFeatArr[i]["cap"] == "true"):
                prevFeatArr[i]["org"] = "true"
                i += 1

    return [prevFeatArr, currFeat, nextFeatArr]

main()
