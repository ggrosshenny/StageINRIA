import Sofa
import os
import sys
from contextlib import contextmanager

class CMTetrahedralCorotationalFEMForceField(Sofa.PythonScriptController):

    def createGraph(self, node):
        # Creation of the 'poutre' node
        self.rootNode = node.getRoot()
        poutreNode = node.createChild('poutre')
        # Add solver
        poutreNode.createObject('EulerImplicit', name='cg_solver', printLog='false')
        poutreNode.createObject('CGLinearSolver', iterations='25', name='linearSolver', tolerance='1.0e-9', threshold='1.0e-9')
        # Mesh loader with physical properties
        poutreNode.createObject('MeshVTKLoader', name='loader', filename='../mesh/poutre2.vtk')
        poutreNode.createObject('Mesh', src='@loader')
        poutreNode.createObject('MechanicalObject', name='mecaObj', src='@loader', dx='2.5')
        # Physic manager
        # Set a topology for boxROI
        # poutreNode.createObject('VolumeTopologyContainer', src='@loader', name='Container')
        # poutreNode.createObject('VolumeTopologyModifier', name='Modifier')
        # poutreNode.createObject('VolumeGeometryAlgorithms', name='GeomAlgo')

        poutreNode.createObject('TetrahedronSetTopologyContainer', src='@loader', name='Container')
        poutreNode.createObject('TetrahedronSetTopologyModifier', name='Modifier')
        poutreNode.createObject('TetrahedronSetTopologyAlgorithms', template='Vec3d', name='TopoAlgo')
        poutreNode.createObject('TetrahedronSetGeometryAlgorithms', template='Vec3d', name='GeomAlgo')

        poutreNode.createObject('CMTetrahedralCorotationalFEMForceField', name='CFEM', youngModulus='1000', poissonRatio='0.2', computeGlobalMatrix='false')

        # BoxROI for fixed constraint (on the left)
        poutreNode.createObject('BoxROI', template='Vec3d', box='2.495 -0.005 -0.005 2.535 0.065 0.0205', drawBoxes='1', position='@mecaObj.position', name='FixedROI', computeTriangles='0', computeTetrahedra='0', computeEdges='0', tetrahedra='@Container.tetrahedra')
        poutreNode.createObject('FixedConstraint', template='Vec3d', name='default6', indices='@FixedROI.indices')
        # BoxROI for constant constraint (on the right)
        poutreNode.createObject('BoxROI', template='Vec3d', box='2.495 -0.005 0.18 2.535 0.065 0.205', drawBoxes='1', position='@mecaObj.rest_position', name='constForceFieldROI', computeTriangles='0', computeTetrahedra='0', computeEdges='0', tetrahedra='@Container.tetrahedra')
        poutreNode.createObject('ConstantForceField', indices='@constForceFieldROI.indices', force='0 0 0.5', arrowSizeCoef='0.1')

        # Visual node
        VisualNode = poutreNode.createChild('Visu')
        VisualNode.createObject('OglModel', name='poutreVisual', fileMesh='../mesh/poutre_surface.obj', color='red', dx='2.5')
        VisualNode.createObject('BarycentricMapping', input='@..', output='@poutreVisual')

        # timer
        Sofa.timerSetInterval("timer_CMTetrahedralCorotationalFEMForceField", 2) # Set the number of steps neded to compute the timer
        Sofa.timerSetEnabled("timer_CMTetrahedralCorotationalFEMForceField", True)

        return 0

    def bwdInitGraph(self, node):
        # Send a message to tester script
        data = ['CMTetrahedralCorotationalFEMForceField.py', 'CMTetrahedralCorotationalFEMForceField']
        self.rootNode.sendScriptEvent('start', data)
        return 0

    def animate(self, iterations):
        # setup the environment
        # Animation loop
        with open("CMTetrahedralCorotationalFEMForceField_SOFATopologyLog.log", "w+") as outputFile :
            outputFile.write("{")
            i = 0
            Sofa.timerSetOutPutType("timer_CMTetrahedralCorotationalFEMForceField", "ljson")
            while i < iterations:
                Sofa.timerBegin("timer_CMTetrahedralCorotationalFEMForceField")
                self.rootNode.simulationStep(0.1)
                result = Sofa.timerEnd("timer_CMTetrahedralCorotationalFEMForceField", self.rootNode)
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
            Sofa.timerSetEnabled("timer_CMTetrahedralCorotationalFEMForceField", 0)
            data = [firstStep]
            self.rootNode.sendScriptEvent('end', data)
        return 0

    def onScriptEvent(self, senderNode, eventName, data):
        if eventName=="CMTetrahedralCorotationalFEMForceField":
            self.animate(data[0])
        return 0
