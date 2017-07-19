# This script is a transcription in .py of the poutre.scn file

import Sofa

class test(Sofa.PythonScriptController):


    #############################################################
    # Method : createGraph                                      #
    # Desc : Called once the script graph is created. Build the #
    #        scene composed of a 'poutre' with two BoxRoi : one #
    #        with 'FixedConstraint' and the other with          #
    #        'ConstantForceField'                               #
    # Param : self - the object itself                          #
    # Param : node - the parent node                            #
    # Return : void                                             #
    #############################################################
    def createGraph(self, node):
        # Creation of the 'poutre' node
        self.rootNode = node.getRoot()
        poutreNode = node.createChild('poutre')
        # Add solver
        poutreNode.createObject('EulerImplicit', name='cg_solver', printLog='false')
        poutreNode.createObject('CGLinearSolver', iterations='25', name='linearSolver', tolerance='1.0e-9', threshold='1.0e-9')
        # Mesh loader with physical properties
        poutreNode.createObject('MeshVTKLoader', name='loader', filename='mesh/poutre2.vtk')
        poutreNode.createObject('Mesh', src='@loader')
        poutreNode.createObject('MechanicalObject', name='mecaObj', src='@loader', dx='2.5')
        # Physic manager
        poutreNode.createObject('TetrahedronFEMForceField', name='FEM', youngModulus='1000', poissonRatio='0.2', computeGlobalMatrix='false', drawAsEdges='true', drawHeterogeneousTetra='true')
        # Set a topology for boxROI
        poutreNode.createObject('TetrahedronSetTopologyContainer', src='@loader', name='Container')
        poutreNode.createObject('TetrahedronSetTopologyModifier', name='Modifier')
        poutreNode.createObject('TetrahedronSetTopologyAlgorithms', template='Vec3d', name='TopoAlgo')
        poutreNode.createObject('TetrahedronSetGeometryAlgorithms', template='Vec3d', name='GeomAlgo')
        poutreNode.createObject('DiagonalMass', template='Vec3d', name='default5', massDensity='0.15')
        # BoxROI for fixed constraint (on the left)
        poutreNode.createObject('BoxROI', template='Vec3d', box='2.495 -0.005 -0.005 2.535 0.065 0.0205', drawBoxes='1', position='@mecaObj.rest_position', name='FixedROI', computeTriangles='0', computeTetrahedra='0', computeEdges='0', tetrahedra='@Container.tetrahedra')
        poutreNode.createObject('FixedConstraint', template='Vec3d', name='default6', indices='@FixedROI.indices')
        # BoxROI for constant constraint (on the right)
        poutreNode.createObject('BoxROI', template='Vec3d', box='2.495 -0.005 0.18 2.535 0.065 0.205', drawBoxes='1', position='@mecaObj.rest_position', name='constForceFieldROI', computeTriangles='0', computeTetrahedra='0', computeEdges='0', tetrahedra='@Container.tetrahedra')
        poutreNode.createObject('ConstantForceField', points='constForceFieldROI.pointsInROI', force='0 0 0.5', arrowSizeCoef='0.1')

        # Visual node
        VisualNode = poutreNode.createChild('Visu')
        VisualNode.createObject('OglModel', name='poutreVisual', fileMesh='mesh/poutre_surface.obj', color='red', dx='2.5')
        VisualNode.createObject('BarycentricMapping', input='@..', output='@poutreVisual')

        return 0

    def bwdInitGraph(self, node):
        # Send a message to tester script
        data = ['test.py', 'test']
        self.rootNode.sendScriptEvent('start', data)

        return 0


    #############################################################
    # Method : simulation                                       #
    # Desc : Call the simulationStep() method until the number  #
    #        of simulation steps is less than *iterations*      #
    #        variable (see global variables). When the          #
    #        condition is completed, send a message to the      #
    #        SceneExecutionTimer script and end the simulation. #
    # Param : void                                              #
    # Return : void                                             #
    #############################################################
    def simulationTest(self, iterations):
        i = 0
        self.rootNode.createChild("ceci_est_un_test")
        while i < iterations:
            self.rootNode.getRoot().simulationStep(0.1)
            i = i+1
        data = [' ']
        self.rootNode.sendScriptEvent('end', data)
        return 0



    #############################################################
    # Method : onScriptEvent                                    #
    # Desc : Called once the right eventName is sent to this    #
    #        script. Call the simulation method.                #
    # Param : self - the object itself                          #
    # Param : senderNode - the sender's node                    #
    # Param : eventName - the event sent to the script          #
    # Param : data - data sent to the script                    #
    # Return : void                                             #
    #############################################################
    def onScriptEvent(self,senderNode,eventName,data):
        if eventName=="test":
            self.simulationTest(data[0])
        return 0
