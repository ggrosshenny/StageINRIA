import Sofa
import os
import sys
from contextlib import contextmanager

class poutreGridSofa(Sofa.PythonScriptController):

    def fileno(self, file_or_fd):
        fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
        if not isinstance(fd, int):
            raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
        return fd

    @contextmanager
    def stdout_redirected(self, to=os.devnull, stdout=None):
        if stdout is None:
           stdout = sys.stdout

        stdout_fd = self.fileno(stdout)
        # copy stdout_fd before it is overwritten
        #NOTE: `copied` is inheritable on Windows when duplicating a standard stream
        with os.fdopen(os.dup(stdout_fd), 'wb') as copied:
            stdout.flush()  # flush library buffers that dup2 knows nothing about
            try:
                os.dup2(self.fileno(to), stdout_fd)  # $ exec >&to
            except ValueError:  # filename
                with open(to, 'wb') as to_file:
                    os.dup2(to_file.fileno(), stdout_fd)  # $ exec > to
            try:
                yield stdout # allow code to be run with the redirected stdout
            finally:
                # restore stdout to its previous value
                #NOTE: dup2 makes stdout_fd inheritable unconditionally
                stdout.flush()
                os.dup2(copied.fileno(), stdout_fd)  # $ exec >&copied

    def createGraph(self, node):

        self.rootNode = node.getRoot()

        # Creation of stuff needed for collision management
        #node.createObject('DefaultAnimationLoop')
        #node.createObject('CollisionPipeline', depth='6', verbose='0', draw='0')
        #node.createObject('BruteForceDetection')
        #node.createObject('CollisionResponse', response='default')
        #node.createObject('DiscreteIntersection')
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

        # timer
        Sofa.timerSetInterval("Animate", 2) # Set the number of steps neded to compute the timer
        Sofa.timerSetEnabled("Animate", 1)


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
            while i < iterations:
                Sofa.timerBegin("Animate")
                self.rootNode.simulationStep(0.1)
                result = Sofa.timerGetTimeAnalysis("Animate", self.rootNode)
                if result != None :
                    outputFile.write(result + ",")
                    oldResult = result
                i = i+1
            print "valeur de oldResult : " + oldResult[-1:]
            last_pose = outputFile.tell()
            outputFile.seek(last_pose - 1)
            outputFile.write("\n}")
            outputFile.close()
            data = [' ']
            self.rootNode.sendScriptEvent('end', data)
        return 0

    def onScriptEvent(self, senderNode, eventName, data):
        if eventName=="poutreGridSofa":
            self.animate(data[0])
        return 0
