import maya.cmds as cmds
import maya.api.OpenMaya as om

class MatBuilder(om.MPxCommand):
    kPluginCmdName = "matBuilder"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return MatBuilder()

    def run(self):
        print("mat builder run")

        if cmds.window("matBuilderWin", exists=True):
            cmds.deleteUI("matBuilderWin")
        cmds.window("matBuilderWin", title="Material Builder", widthHeight=(200, 100))
        cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="Hello mat builder")
        cmds.showWindow("matBuilderWin")
