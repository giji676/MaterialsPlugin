import maya.cmds as cmds
import maya.api.OpenMaya as om

class MatSelector(om.MPxCommand):
    kPluginCmdName = "matSelector"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return MatSelector()

    def run(self):
        print("mat selector run")

        if cmds.window("matSelectorWin", exists=True):
            cmds.deleteUI("matSelectorWin")
        cmds.window("matSelectorWin", title="Material Selector", widthHeight=(200, 100))
        cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="Hello mat selector")
        cmds.showWindow("matSelectorWin")
