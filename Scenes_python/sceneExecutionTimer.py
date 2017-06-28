import Sofa
import sys
from time import clock

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
    reduce(lambda ll,b : divmod(ll[0],b) + ll[1:], [(t*1000,),1000,60,60])

class SceneExecutionTimer(Sofa.PythonScriptController):

    start = 0
    end = 0

    #Called once the script is loaded
    def onLoaded(self, node):
        print '########## Scene execution timer script ##########'
        print '### This script will calculate the execution time of a SOFA/CIGOGN script'
        print '##################################################'

        # Create node for the script
        self.rootNode = node.getRoot()
        scriptToTestNode = self.rootNode.getChild('Script_to_test_node')
        if scriptToTestNode != None:
            ScriptObj = scriptToTestNode.getObject('ScriptToTest')
            if ScriptObj != None:
                fileName = ScriptObj.findData('filename').value
                className = ScriptObj.findData('classname').value
            else:
                print "Error : PythonScriptController not found"
        else:
            print "Error : test script node not found"

        # create execution log file
        try:
            logsFile = open("Logs/"+fileName+"_"+className+"_benchmark.log", "w+")
        except IOError as e:
            print "I/O error ({0}) : {1}".format(e.errno, e.strerror)
            raise

        # Write the actual time in the logs file
        try:
            start = clock()
            logsFile.write("Begin at: " + secondsToStr(start))
        except IOError as e:
            print "I/O error ({0}) : {1}".format(e.errno, e.strerror)
            raise

        # call the script to test
        data = ['SceneExecutionTimer', scriptToTestNode]
        self.rootNode.sendScriptEvent(str(className), data)

        return 0

    def onScriptEvent(self,senderNode,eventName,data):
        if eventName=='end':
            # Write the actual time in the logs file
            try:
                end = clock()
                logsFile.write("End at: " + secondsToStr(end))
            except IOError as e:
                print "I/O error ({0}) : {1}".format(e.errno, e.strerror)
                raise
            # Calculate the execution time
            executionTime = end-start
            logsFile.write("total time: " + str(executionTime))

            # Close the file
            logsFile.close()
