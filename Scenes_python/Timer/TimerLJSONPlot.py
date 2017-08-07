import sys
import matplotlib.pyplot as plt
from collections import OrderedDict
import json

class TimerLJSONPlot() :

    def __init__(self):
        lol = 0


    ###
     # Method : parseJsonComponantsId
     # Brief : parse a json file to create a block for the given composant name
     # Param : jsonData, json - data extracted from the json file
     # Param : componantID, string - id of the component to seek in the json file
     # Param : deep, int - 0 to get all componants on the same level than target, 1 to get all children of target
     ###
    def parseJsonComponantsId(self, jsonData, componantID, deep) :
        parsedInformations = []

        # First iteration is used to create the list that will handle informations
        # The list is defiend as following :
        #     steps   | componantID | subComponant | subComponant2 | ...
        # 0  "Steps"  |  "CompName" | "subCompName"| "subCompName" | ...
        # 1     1     |    0.285    |      0.185   |      0.1      | ...
        #                        ...

        keyNumber = 0
        father = ""

        # Each k in this loop is the simulation step
        for k,v in jsonData.items() :

            # First analys to take search informations
            if keyNumber == 0 :
                row = ["Steps", k]
                parsedInformations.append(row)
                # Take informations from the target componant
                for kbis, vbis in v.items() :
                    if kbis == componantID :
                        if deep == 0 :
                            father = vbis["Father"]
                        else :
                            father = componantID
                        row = []
                        row.append(componantID)
                        row.append(vbis["Values"]["Percent"])
                        parsedInformations.append(row)
                # Take informations from componants on the same level than the target
                for kbis, vbis in v.items() :
                    if kbis != componantID and vbis["Father"] == father :
                        row = []
                        row.append(kbis)
                        row.append(vbis["Values"]["Percent"])
                        parsedInformations.append(row)
                keyNumber = 1

            # Informations extraction
            else :
                parsedInformations[0].append(int(k))
                for kbis, vbis in v.items() :
                    i = 0
                    if kbis == componantID or vbis["Father"] == father :
                        # Find the componant index in parsedInformations
                        for j, info in enumerate(parsedInformations) :
                            if info[0] == kbis :
                                i = j
                        # stock informations
                        row = parsedInformations[i]
                        row.append(vbis["Values"]["Percent"])

        return parsedInformations


    ###
     # Method : parseJsonFile
     # Brief : parse a json file to create a gnuplot file of the timer analysis
     # Param : jsonFile, string - name of the file to parse
     # Param : *componantsID, list of strings - ids of components to seek in the file
     ###
    def parseJsonFile(self, jsonFileName, deep, *componantsID):
        with open(jsonFileName, "r")  as jsonFile :
            jsonData = json.load(jsonFile, object_pairs_hook=OrderedDict)

            fig, ax = plt.subplots()
            for componantID in componantsID :
                test = self.parseJsonComponantsId(jsonData, componantID, deep)
            # Create plot
                for i in test :
                    if i[0] != "Steps" :
                        ax.plot(test[0][1:], i[1:], label=i[0])
            legend = ax.legend(loc='best', shadow=True, fontsize='x-large')
            legend.get_frame().set_facecolor('#00FFCC')
            plt.show()

            jsonFile.close()

        return 0
