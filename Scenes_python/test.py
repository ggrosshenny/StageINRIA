# This script is a transcription in .py of the poutre.scn file

import Sofa

class test(Sofa.PythonScriptController):

    def onScriptEvent(self,senderNode,eventName,data):
        if eventName=="test":
            # Creation of stuff needed for collision management
            node = data[1].getRoot()
            #node.createObject('CollisionPipeline', depth='6', verbose='0', draw='0')
            #node.createObject('BruteForceDetection')
            #node.createObject('NewProximityIntersection', alarmDistance='0.3', contactDistance='0.2')
            #node.createObject('CollisionResponse', response='false')
            #node.createObject('CollisionGroup')

            # Creation of the 'poutre' node
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
