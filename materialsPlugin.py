import sys
import maya.api.OpenMaya as om
import maya.cmds as cmds
from matSelector import MatSelector
from matBuilder import MatBuilder

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass

def open_material_selector(*args):
    mat_selector = MatSelector()
    mat_selector.run()

def open_material_builder(*args):
    mat_builder = MatBuilder()
    mat_builder.run()

def initializePlugin(plugin):
    vendor = "GIJI676"
    version = "0.0.1"
    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    try:
        if not cmds.menu("MaterialsPlugin", exists=True):
            cmds.menu("MaterialsPlugin", label="Materials Plugin", parent="MayaWindow", tearOff=True)

        cmds.menuItem(
            label="Open Material Selector",
            parent="MaterialsPlugin",
            command=open_material_selector,
        )
        cmds.menuItem(
            label="Open Material Builder",
            parent="MaterialsPlugin",
            command=open_material_builder,
        )

        plugin_fn.registerCommand(MatSelector.kPluginCmdName, MatSelector.cmdCreator)
        plugin_fn.registerCommand(MatBuilder.kPluginCmdName, MatBuilder.cmdCreator)

    except Exception as e:
        sys.stderr.write(
            f"Failed to register commands: {e}\n"
        )
        raise

def uninitializePlugin(plugin):
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(MatSelector.kPluginCmdName)
        plugin_fn.deregisterCommand(MatBuilder.kPluginCmdName)

    except Exception as e:
        sys.stderr.write(
            f"Failed to unregister commands: {e}\n"
        )
        raise
