import Sofa

class SceneManager(Sofa.PythonScriptController):

    def onScriptEvent(self,senderNode,eventName,data):
        rootNode = senderNode.getRoot()
        if eventName=="start":
            # call the script to test
            iterations = 10
            sentData = [iterations]
            rootNode.sendScriptEvent(str(data[1]), sentData)

        if eventName=='end':
            print "end of the test"

        return 0
