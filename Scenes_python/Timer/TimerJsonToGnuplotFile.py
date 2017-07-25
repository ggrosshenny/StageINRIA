import sys
import json

class TimerJsonToGnuplotFile() :


    ###
     # Method : parseJsonComponantsId
     # Brief : parse a json file to create a block for the given composant name
     # Param : jsonData, json - data extracted from the json file
     # Param : outPutFile, filedDescriptor - file descriptor of th gnuplot output file
     # Param : stepsnumber, int - number of steps of the simulation
     # Param : timerInterval, int - interval of the AdvancedTimer
     # Param : componantID, string - id of the component to seek in the json file
     ###
    def parseJsonComponantsId(jsonData, outPutFile, stepsnumber, timerInterval, componantID) :
        # Write the block name
        blockName = '\"' + componantID + '\"\n'
        outPutFile.write(blockName)

        # Write block data in the given output file
        i = 0
        while(i <= stepsnumber)
        {
            data = i + " " + jsonData[i][componantID]["Percent"] + "\n"
            outPutFile.werite(data)
            i += timerInterval
        }

        outPutFile.write("\n\n") # End of block
        return 0


    ###
     # Method : parseJsonFile
     # Brief : parse a json file to create a gnuplot file of the timer analysis
     # Param : jsonFile, string - name of the file to parse
     # Param : stepsnumber, int - number of steps of the simulation
     # Param : timerInterval, int - interval of the AdvancedTimer
     # Param : *componantsID, list of strings - ids of components to seek in the file
     ###
    def parseJsonFile(self, jsonFileName, stepsnumber, timerInterval, *componantsID):
        with open(jsonFileName, "r"), open((jsonFileName + "_gnuplot.plot"), "w+") as jsonFile, gnuplotFile:
            jsonData = json.load(jsonFile)

            for componantID in componantsID :
                parseJsonComponantsId(jsonData, outPutFile, stepsnumber, timerInterval, componantID)
            
            jsonFile.close()
            gnuplotFile.close()
        return 0
