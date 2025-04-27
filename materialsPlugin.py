import sys
import maya.api.OpenMaya as om
import maya.cmds as cmds
from matSelector import MatSelector
from matBuildSelector import BuildMaterial, MatBuildSelector

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass

def reload_materials_plugin(*args):
    print("Reloading materialsPlugin")
    plugin_name = "materialsPlugin.py"

    if cmds.pluginInfo(plugin_name, query=True, loaded=True):
        cmds.unloadPlugin(plugin_name)

    cmds.refresh()
    import time
    time.sleep(1.5)

    for module_name in ["matSelector", "matBuildSelector", "buildMaterial", "materialsPlugin"]:
        if module_name in sys.modules:
            del sys.modules[module_name]

    cmds.loadPlugin(plugin_name)

def open_material_selector(*args):
    mat_selector = MatSelector()
    mat_selector.run()

def open_material_builder(*args):
    mat_builder = MatBuildSelector()
    mat_builder.run()

def initializePlugin(plugin):
    vendor = "GIJI676"
    version = "0.0.1"
    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    try:
        if not cmds.menu("MaterialsPlugin", exists=True):
            cmds.menu("MaterialsPlugin", label="Materials Plugin", parent="MayaWindow", tearOff=True)

        cmds.menuItem(
            "matSelectorItem",
            label="Open Material Selector",
            parent="MaterialsPlugin",
            command=open_material_selector,
        )
        cmds.menuItem(
            "matBuilderItem",
            label="Open Material Builder",
            parent="MaterialsPlugin",
            command=open_material_builder,
        )
        cmds.menuItem(
            "reloadPluginItem",
            label="Reload Plugin",
            parent="MaterialsPlugin",
            command=reload_materials_plugin,
        )

        plugin_fn.registerCommand(MatSelector.kPluginCmdName, MatSelector.cmdCreator)
        plugin_fn.registerCommand(MatBuildSelector.kPluginCmdName, MatBuildSelector.cmdCreator)
        plugin_fn.registerCommand(BuildMaterial.kPluginCmdName, BuildMaterial.cmdCreator)

    except Exception as e:
        sys.stderr.write(
            f"Failed to register commands: {e}\n"
        )
        raise

def uninitializePlugin(plugin):
    plugin_fn = om.MFnPlugin(plugin)
    try:
        if cmds.menuItem("matSelectorItem", exists=True):
            cmds.deleteUI("matSelectorItem")
        if cmds.menuItem("matBuilderItem", exists=True):
            cmds.deleteUI("matBuilderItem")
        if cmds.menuItem("reloadPluginItem", exists=True):
            cmds.deleteUI("reloadPluginItem")
        if cmds.menu("MaterialsPlugin", exists=True):
            cmds.deleteUI("MaterialsPlugin", menu=True)

        plugin_fn.deregisterCommand(MatSelector.kPluginCmdName)
        plugin_fn.deregisterCommand(MatBuildSelector.kPluginCmdName)
        plugin_fn.deregisterCommand(BuildMaterial.kPluginCmdName)

    except Exception as e:
        sys.stderr.write(
            f"Failed to unregister commands: {e}\n"
        )
        raise
