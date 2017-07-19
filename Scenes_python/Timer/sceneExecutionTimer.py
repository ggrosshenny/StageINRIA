import Sofa
import sys
import os
from time import clock

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
    reduce(lambda ll,b : divmod(ll[0],b) + ll[1:], [(t*1000,),1000,60,60])

class SceneExecutionTimer(Sofa.PythonScriptController):

    start = 0
    end = clock()
    try:
        logsFile = open(" ", "w+")
    except IOError as e:
        pass
    currentFilePath = os.path.dirname(os.path.abspath(__file__))

    #Called once the script is ready
    def onScriptEvent(self,senderNode,eventName,data):
        if eventName=="start":
            iterations = 10000
            print '########## Scene execution timer script ##########'
            print '### This script will calculate the execution time of a SOFA/CIGOGN script for 10 000 animation steps'
            print '##################################################'
            print "current file path : " + self.currentFilePath
            # Create node for the script
            rootNode = senderNode.getRoot()
            # Create logsFile
            try:
                self.logsFile = open(self.currentFilePath + "/Logs/" + data[0] + "_" + data[1] + "_benchmark.log", "w+")

            except IOError as e:
                print "I/O error ({0}) : {1}".format(e.errno, e.strerror)
                raise
            # Write the actual time in the logs file
            try:
                print "valeur de end: " + str(self.end)
                self.start = clock()
                self.logsFile.write("Begin at: " + secondsToStr(self.start) + "\n")
            except IOError as e:
                print "I/O error ({0}) : {1}".format(e.errno, e.strerror)
                raise
            # call the script to test
            sentData = [iterations]
            rootNode.sendScriptEvent(str(data[1]), sentData)

        if eventName=='end':
            # Write the actual time in the logs file
            try:
                self.end = clock()
                self.logsFile.write("End at: " + secondsToStr(self.end) + "\n")
            except IOError as e:
                print "I/O error ({0}) : {1}".format(e.errno, e.strerror)
                raise
            # Calculate the execution time
            executionTime = self.end-self.start
            self.logsFile.write("total time: " + str(executionTime))

            # Close the file
            self.logsFile.close()
            print "The execution time was " + str(executionTime) + " s."

        return 0
