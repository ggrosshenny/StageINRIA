import sys
import json

class TimerJsonToGnuplotFile() :

    def __init__(self):
        lol = 0


    ###
     # Method : findKey
     # Brief : find the given key from a given json data
     # Param : jsonData, json - data extracted from the json file
     # Param : key, the key to find
     ###
    def findKey(self, jsonData, key) :
        currentlevelKeysValue = []

        for k, v in jsonData.items() :
            # Keep the keys for deep travel
            if k != key and k != "Values" :
                print "voici la cle : " + str(k) + "\n"
                currentlevelKeysValue.append(v)
            # If the key was found
            elif k != "Values" :
                print "voici la cle : " + str(k) + "\n"
                return v

        # If the key was not found and there is
        if len(currentlevelKeysValue) != 0 :
            for e in currentlevelKeysValue :
                return self.findKey(e, key)

        # The key doesn't exist in the json
        return None


    ###
     # Method : parseJsonComponantsId
     # Brief : parse a json file to create a block for the given composant name
     # Param : jsonData, json - data extracted from the json file
     # Param : outPutFile, filedDescriptor - file descriptor of th gnuplot output file
     # Param : stepsnumber, int - number of steps of the simulation
     # Param : timerInterval, int - interval of the AdvancedTimer
     # Param : componantID, string - id of the component to seek in the json file
     ###
    def parseJsonComponantsId(self, jsonData, outPutFile, firstStep, stepsnumber, timerInterval, componantID) :
        parsedInformations = []

        # First iteration is used to create the list that will handle informations
        # The list is defiend as following :
        #   step | componantID | subComponant | subComponant2 | ...
        # 0  ""  |  "CompName" | "subCompName"| "subCompName" | ...
        # 1  1   |    0.285    |      0.185   |      0.1      | ...
        #                        ...

        print "\nthe key value : " + json.dumps(self.findKey(jsonData[str(firstStep)], componantID), indent=4) + "\n"

        return 0


    ###
     # Method : parseJsonFile
     # Brief : parse a json file to create a gnuplot file of the timer analysis
     # Param : jsonFile, string - name of the file to parse
     # Param : stepsnumber, int - number of steps of the simulation
     # Param : timerInterval, int - interval of the AdvancedTimer
     # Param : *componantsID, list of strings - ids of components to seek in the file
     ###
    def parseJsonFile(self, jsonFileName, firstStep, stepsnumber, timerInterval, *componantsID):
        with open(jsonFileName, "r")  as jsonFile :
            with open(("../TimerLogs/" + jsonFileName + "_gnuplot.plot"), "w+") as gnuplotFile:
                jsonData = json.load(jsonFile)

                for componantID in componantsID :
                    self.parseJsonComponantsId(jsonData, gnuplotFile, firstStep, stepsnumber, timerInterval, componantID)

                gnuplotFile.close()
            jsonFile.close()

        return 0
