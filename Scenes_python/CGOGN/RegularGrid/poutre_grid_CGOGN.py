import Sofa

def createScene(node):
    # Creation of stuff needed for collision management
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
    poutreRegGridNode.createObject('RegularGrid', name='regGrid', nx='3', ny='5', nz='10', min='1.995 -0.005 -0.005', max='2.035 0.065 0.205')
    # Physic manager
    poutreRegGridNode.createObject('HexahedronFEMForceField', name='HFEM', youngModulus='1000', poissonRatio='0.2')

    # Set a topology for boxROI
    poutreRegGridNode.createObject('VolumeTopologyContainer', src='@regGrid', name='Container')
    poutreRegGridNode.createObject('HexahedronSetTopologyModifier', name='Modifier')
    poutreRegGridNode.createObject('HexahedronSetTopologyAlgorithms', template='Vec3d', name='TopoAlgo')
    poutreRegGridNode.createObject('HexahedronSetGeometryAlgorithms', template='Vec3d', name='GeomAlgo')

    # BoxConstraint for fixed constraint (on the left)
    poutreRegGridNode.createObject('BoxROI', name="FixedROI", box="1.995 -0.005 -0.005 2.035 0.065 0.0205", position='@mecaObj.rest_position')
    poutreRegGridNode.createObject('FixedConstraint', template='Vec3d', name='default6', indices='@FixedROI.indices')
    # BoxROI for constant constraint (on the right)
    poutreRegGridNode.createObject('BoxROI', template='Vec3d', box='1.995 -0.005 0.18 2.035 0.065 0.205', name='box_roi2', position='@mecaObj.rest_position')
    poutreRegGridNode.createObject('ConstantForceField', points="@box_roi2.indices", force='0 -0.1 0', arrowSizeCoef='0.01')

    # Visual node
    VisualNode = poutreRegGridNode.createChild('Visu')
    VisualNode.createObject('OglModel', name='poutreRegGridVisual', fileMesh='mesh/poutre_surface.obj', color='red', dx='2.5')
    VisualNode.createObject('BarycentricMapping', input='@..', output='@poutreRegGridVisual')
