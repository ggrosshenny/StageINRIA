import Sofa
import TimerLJSONPlot

class SceneManager(Sofa.PythonScriptController):

    def onScriptEvent(self,senderNode,eventName,data):
        rootNode = senderNode.getRoot()
        if eventName=="start":
            # call the script to test
            iterations = 1000
            sentData = [iterations]
            rootNode.sendScriptEvent(str(data[1]), sentData)

        if eventName=='end':
            print "end of the test"
            test = TimerLJSONPlot.TimerLJSONPlot()
            test.parseJsonFile("poutre_grid_CGOGN_timerLog.log", 0, "Mechanical")

        return 0
