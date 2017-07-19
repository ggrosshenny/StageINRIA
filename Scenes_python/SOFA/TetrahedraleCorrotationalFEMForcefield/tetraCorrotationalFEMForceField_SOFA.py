# This script is a transcription in .py of the poutre.scn file with TetrahedralCorotationalFEMForceField

import Sofa

#############################################################
# Method : onLoaded                                         #
# Desc : Called once the script is loaded. Build the scene  #
#        composed of a 'poutre' with two BoxRoi : one with  #
#        'FixedConstraint' and the other with               #
#        'ConstantForceField'                               #
# Param : self - the object itself                          #
# Param : node - the parent node                            #
# Return : void                                             #
#############################################################
def createScene(node):
    # Creation of the 'poutre' node
    node = node.createChild('poutre')
    # Add solver
    node.createObject('EulerImplicit', name='cg_solver', printLog='false')
    node.createObject('CGLinearSolver', iterations='25', name='linearSolver', tolerance='1.0e-9', threshold='1.0e-9')
    # Mesh loader with physical properties
    node.createObject('MeshVTKLoader', name='loader', filename='mesh/poutre2.vtk')
    node.createObject('Mesh', src='@loader')
    node.createObject('MechanicalObject', name='mecaObj', src='@loader', dx='2.5')
    # Physic manager
    node.createObject('TetrahedralCorotationalFEMForceField', name='CFEM', youngModulus='1000', poissonRatio='0.2', drawAsEdges='true', drawHeterogeneousTetra='true')
    # Set a topology for boxROI
    node.createObject('TetrahedronSetTopologyContainer', src='@loader', name='Container')
    node.createObject('TetrahedronSetTopologyModifier', name='Modifier')
    node.createObject('TetrahedronSetTopologyAlgorithms', template='Vec3d', name='TopoAlgo')
    node.createObject('TetrahedronSetGeometryAlgorithms', template='Vec3d', name='GeomAlgo')
    node.createObject('DiagonalMass', template='Vec3d', name='default5', massDensity='0.15')
    # BoxROI for fixed constraint (on the left)
    node.createObject('BoxROI', template='Vec3d', box='1.995 -0.005 -0.005 2.035 0.065 0.0205', drawBoxes='1', position='@mecaObj.rest_position', name='FixedROI', computeTriangles='0', computeTetrahedra='0', computeEdges='0', tetrahedra='@Container.tetrahedra')
    node.createObject('FixedConstraint', template='Vec3d', name='default6', indices='@FixedROI.indices')
    # BoxROI for constant constraint (on the right)
    node.createObject('BoxROI', template='Vec3d', box='1.995 -0.005 0.18 2.035 0.065 0.205', drawBoxes='1', position='@mecaObj.rest_position', name='constForceFieldROI', computeTriangles='0', computeTetrahedra='0', computeEdges='0', tetrahedra='@Container.tetrahedra')
    node.createObject('ConstantForceField', points='constForceFieldROI.pointsInROI', force='0 0 0.5', arrowSizeCoef='0.1')

    # Visual node
    VisualNode = node.createChild('Visu')
    VisualNode.createObject('OglModel', name='poutreVisual', fileMesh='mesh/poutre_surface.obj', color='red', dx='2.5')
    VisualNode.createObject('BarycentricMapping', input='@..', output='@poutreVisual')

    return 0
