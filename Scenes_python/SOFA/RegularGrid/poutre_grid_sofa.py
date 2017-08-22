import Sofa
import os
import sys
from contextlib import contextmanager

class poutreGridSofa(Sofa.PythonScriptController):

    def createGraph(self, node):

        self.rootNode = node.getRoot()

        # Creation of stuff needed for collision management
        node.createObject('DefaultAnimationLoop')
        node.createObject('CollisionPipeline', depth='6', verbose='0', draw='0')
        node.createObject('BruteForceDetection')
        node.createObject('CollisionResponse', response='default')
        node.createObject('DiscreteIntersection')
        node.createObject('VisualStyle', displayFlags="showBehaviorModels showForceFields showVisual" )

        # Creation of the 'poutreRegGrid' node
        poutreRegGridNode = node.createChild('poutreRegGrid')
        # Add solver
        poutreRegGridNode.createObject('EulerImplicit', name='cg_solver', printLog='false')
        poutreRegGridNode.createObject('CGLinearSolver', iterations='25', name='linearSolver', tolerance='1.0e-9', threshold='1.0e-9')
        # Creation of the regular grid
        poutreRegGridNode.createObject('MechanicalObject', name='mecaObj')
        poutreRegGridNode.createObject('RegularGrid', name='regGrid', nx='3', ny='5', nz='10', min='2.495 -0.005 -0.005', max='2.535 0.065 0.205')
        # Set a topology for boxROI
        poutreRegGridNode.createObject('HexahedronSetTopologyContainer', src='@regGrid', name='Container')
        poutreRegGridNode.createObject('HexahedronSetTopologyModifier', name='Modifier')
        poutreRegGridNode.createObject('HexahedronSetTopologyAlgorithms', template='Vec3d', name='TopoAlgo')
        poutreRegGridNode.createObject('HexahedronSetGeometryAlgorithms', template='Vec3d', name='GeomAlgo')
        # Physic manager
        poutreRegGridNode.createObject('HexahedronFEMForceField', name='HFEM', youngModulus='1000', poissonRatio='0.2')
        # BoxConstraint for fixed constraint (on the left)
        poutreRegGridNode.createObject('BoxROI', name="FixedROI", box="2.495 -0.005 -0.005 2.535 0.065 0.0205", position='@mecaObj.rest_position')
        poutreRegGridNode.createObject('FixedConstraint', template='Vec3d', name='default6', indices='@FixedROI.indices')
        # BoxROI for constant constraint (on the right)
        poutreRegGridNode.createObject('BoxROI', template='Vec3d', box='2.495 -0.005 0.18 2.535 0.065 0.205', name='box_roi2', position='@mecaObj.rest_position')
        poutreRegGridNode.createObject('ConstantForceField', indices="@box_roi2.indices", force='0 -0.1 0', arrowSizeCoef='0.01')

        # Visual node
        VisualNode = poutreRegGridNode.createChild('Visu')
        VisualNode.createObject('OglModel', name='poutreRegGridVisual', fileMesh='../mesh/poutre_surface.obj', color='red', dx='2.5')
        VisualNode.createObject('BarycentricMapping', input='@..', output='@poutreRegGridVisual')
        VisualNode.createObject('STLExporter', position="@poutreRegGridVisual.position", filename="../ModelsTimer/SOFA/poutre_grid_sofa_model", exportEveryNumberOfSteps='1', exportAtEnd="1", triangle="@poutreRegGridVisual.triangles", listening="1")

        # timer
        Sofa.timerSetInterval("timer_poutre_grid_sofa", 2) # Set the number of steps neded to compute the timer
        Sofa.timerSetEnabled("timer_poutre_grid_sofa", True)


    def bwdInitGraph(self, node):
        # Send a message to tester script
        data = ['poutre_grid_sofa.py', 'poutreGridSofa']
        self.rootNode.sendScriptEvent('start', data)
        return 0


    def animate(self, iterations):
        #setup the environment
        #Animation loop
        with open("poutre_grid_sofa_timerLog.log", "w+") as outputFile :
            outputFile.write("{")
            i = 0
            Sofa.timerSetOutPutType("timer_poutre_grid_sofa", "ljson")
            while i < iterations:
                Sofa.timerBegin("timer_poutre_grid_sofa")
                self.rootNode.simulationStep(0.1)
                result = Sofa.timerEnd("timer_poutre_grid_sofa", self.rootNode)
                if result != None :
                    outputFile.write(result + ",")
                    oldResult = result
                i = i+1
            last_pose = outputFile.tell()
            outputFile.seek(last_pose - 1)
            outputFile.write("\n}")
            outputFile.seek(7)
            firstStep = outputFile.read(1)
            outputFile.close()
            Sofa.timerSetEnabled("timer_poutre_grid_sofa", 0)

            data = [firstStep]
            self.rootNode.sendScriptEvent('end', data)
        return 0

    def onScriptEvent(self, senderNode, eventName, data):
        if eventName=="poutreGridSofa":
            self.animate(data[0])
        return 0
