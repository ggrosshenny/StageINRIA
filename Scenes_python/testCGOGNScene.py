# This scene is a test of CGOGN

import Sofa


def createScene(node):
    # add some settings
    node.createObject('CollisionPipeline', depth='6', verbose='0', draw='0')
    node.createObject('BruteForceDetection')
    node.createObject('NewProximityIntersection', alarmDistance='0.3', contactDistance='0.2')
    node.createObject('CollisionResponse', response='false')
    node.createObject('CollisionGroup')
    # Creation of the 'poutre' node
    poutreNode = node.createChild('poutreNode')
    # Add solver
    poutreNode.createObject('EulerImplicit', name='cg_solver', printLog='false')
    poutreNode.createObject('CGLinearSolver', iterations='25', name='linearSolver', tolerance='1.0e-9', threshold='1.0e-9')
    # Mesh loader with physical properties
    poutreNode.createObject('MeshVTKLoader', name='loader', filename='mesh/poutre2.vtk')
    poutreNode.createObject('Mesh', src='@loader')
    poutreNode.createObject('MechanicalObject', name='mecaObj', src='@loader', dx='2.5')
    # Topology settings
    poutreNode.createObject('VolumeTopologyContainer', src='@loader', name='Container', tetrahedra='@loader.tetrahedra')
    # Physic manager
    poutreNode.createObject('CMTetrahedralCorotationalFEMForceField', name='CMCFEM', youngModulus='360', poissonRatio='0.3', method='large')
    # Set CGOGN topology
    #poutreNode.createObject('TetrahedronSetTopologyModifier', name='Modifier')
    #poutreNode.createObject('TetrahedronSetGeometryAlgorithms', template='Vec3d', name='GeomAlgo')

    # Visual node
    VisualNode = poutreNode.createChild('Visu')
    VisualNode.createObject('OglModel', name='poutreVisual', fileMesh='mesh/poutre_surface.obj', color='red', dx='2.5')
    VisualNode.createObject('BarycentricMapping', input='@..', output='@poutreVisual')

    return 0
