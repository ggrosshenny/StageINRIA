import sys
import matplotlib.pyplot as plt
from collections import OrderedDict
import json

class TimerLjsonTwoFilesPlot() :

    def __init__(self):
        lol = 0


    ###
     # Method : parseJsonComponantsId
     # Brief : parse a json file to create a block for the given composant name
     # Param : jsonData, json - data extracted from the json file
     # Param : componantID, string - id of the component to seek in the json file
     # Param : deep, int - 0 to get all componants on the same level than target, 1 to get all children of target
     ###
    def parseJsonComponantsId(self, jsonData, *componantsID) :

        # First iteration is used to create the list that will handle informations
        # The list is defiend as following :
        #     steps   | componantID |
        # 0  "Steps"  |  "CompName" |
        # 1     1     |    0.285    |
        #            ...

        parsedInformations = []
        firstPass = 1

        # Each k in this loop is the simulation step
        for k,v in jsonData.items() :

            # First analys to take Steps informations
            if firstPass == 1 :
                row = ["Steps", k]
                parsedInformations.append(row)
                # Take informations from the target componant
                for kbis, vbis in v.items() :
                    for key in componantsID :
                        if kbis == key :
                            row = []
                            row.append(key)
                            row.append(vbis["Values"]["Percent"])
                            parsedInformations.append(row)
                firstPass = 0

            # Informations extraction
            else :
                parsedInformations[0].append(int(k))
                for kbis, vbis in v.items() :
                    i = 0
                    for key in componantsID :
                        if kbis == key :
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
    def parseJsonFile(self, firstJsonFileName, secondJsonFileName, *componantsID):
        with open(firstJsonFileName, "r")  as firstJsonFile :
            firsFileJsonData = json.load(firstJsonFile, object_pairs_hook=OrderedDict)

            with open(secondJsonFileName, "r")  as secondJsonFile :
                secondFileJsonData = json.load(secondJsonFile, object_pairs_hook=OrderedDict)

                # First file plot :
                firsFileInformations = self.parseJsonComponantsId(firsFileJsonData, *componantsID)
                # Second file plot :
                secondFileInformations = self.parseJsonComponantsId(secondFileJsonData, *componantsID)

                fig, ax = plt.subplots()
                lineColors = ["green", "blue"]
                markStyles = ['.', '+', 'p', '*', 'o', 'v', '^', '<', '>', '8', 's', 'h', 'x', 'D', '2']
                lineColorIndice = 0
                markStyleIndice = 0

                # First file part
                for i in firsFileInformations :
                    if i[0] != "Steps" :
                        labelName = firstJsonFileName + "::" + i[0]
                        ax.plot(firsFileInformations[0][1:], i[1:], label=labelName, color=lineColors[lineColorIndice], marker=markStyles[markStyleIndice])
                        markStyleIndice = (markStyleIndice + 1) % len(markStyles)

                # Second file part
                lineColorIndice = lineColorIndice + 1
                markStyleIndice = 0
                for i in secondFileInformations :
                    if i[0] != "Steps" :
                        labelName = secondJsonFileName + "::" + i[0]
                        ax.plot(secondFileInformations[0][1:], i[1:], label=labelName, color=lineColors[lineColorIndice], marker=markStyles[markStyleIndice])
                        markStyleIndice = (markStyleIndice + 1) % len(markStyles)

                # Create the legend of the plot
                legend = ax.legend(loc='best', shadow=True, fontsize='x-large')

                #legend.get_frame().set_facecolor('#00FFCC')
                plt.show()

                secondJsonFile.close()
            firstJsonFile.close()

        return 0
