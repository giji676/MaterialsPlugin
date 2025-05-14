import os
import shutil
import zipfile
import maya.cmds as cmds
import maya.api.OpenMaya as om

from buildMaterial import BuildMaterial

class MatBuildSelector(om.MPxCommand):
    kPluginCmdName = "matBuildSelector"
    def __init__(self):
        om.MPxCommand.__init__(self)
        self.window = None
        self.lyt_grid = None
        self.lbl_folder = None
        self.lbl_zip = None
        self.lbl_output_path = None
        self.lbl_status_update = None

        self.input_path = ""
        self.zip_input_path = ""
        self.output_path = ""
        self.is_zip = False

        self.build_material_window()

    @staticmethod
    def cmdCreator():
        return MatBuildSelector()

    def run(self):
        pass

    def update_path_lbls(self):
        if self.is_zip:
            cmds.text(self.lbl_folder, edit=True, label="")
            cmds.text(self.lbl_zip, edit=True, label=self.input_path)
        else:
            cmds.text(self.lbl_zip, edit=True, label="")
            cmds.text(self.lbl_folder, edit=True, label=self.input_path)

    def open_folder_selector_dialog(self, *args):
        selected = cmds.fileDialog2(
            caption="Select Material Folder",
            fileMode=2,  # 2 = Select only folder
            okCaption="Select"
        )

        if selected:
            self.input_path = selected[0]
            self.zip_input_path = ""
            self.is_zip = False
            self.update_path_lbls()

    def open_zip_selector_dialog(self, *args):
        selected = cmds.fileDialog2(
            caption="Select Folder or ZIP File",
            fileMode=4,
            okCaption="Select",
            fileFilter="ZIP Files (*.zip)"
        )

        if selected:
            self.input_path = selected[0]
            self.zip_input_path = selected[0]
            self.is_zip = True
            self.update_path_lbls()

    def open_output_folder_selector_dialog(self, *args):
        selected = cmds.fileDialog2(
            caption="Select Output Folder",
            fileMode=2,  # 2 = Select only folder
            okCaption="Select"
        )

        if selected:
            self.output_path = selected[0]
            cmds.text(self.lbl_output_path, edit=True, label=self.output_path)

    def unzip(self, inp, output):
        if output == "":
            cmds.inViewMessage(amg=f"Please select the output path", pos='midCenter', fade=True)
            return
        if not os.path.exists(inp):
            cmds.inViewMessage(amg=f"File '{inp}' not found", pos='midCenter', fade=True)
            return
        if not os.path.exists(output):
            os.mkdir(output)

        cmds.text(self.lbl_status_update, edit=True, label="Unzipping")
        with zipfile.ZipFile(inp, 'r') as zip_ref:
            zip_ref.extractall(output)
            self.rename_inside_dir(output)

    def rename_inside_dir(self, path):
        name = os.path.basename(path)

        for file in os.listdir(path):
            ext = os.path.splitext(file)[1]
            if os.path.splitext(file)[0] == ".mayaSwatches":
                continue
            file_path = os.path.join(path, file)

            if "displacement" in file.lower():
                new_file_path = os.path.join(path, f"{name}_displacement{ext}")
            elif "roughness" in file.lower():
                new_file_path = os.path.join(path, f"{name}_roughness{ext}")
            elif "normalgl" in file.lower():
                new_file_path = os.path.join(path, f"{name}_normalgl{ext}")
            elif "normald" in file.lower():
                new_file_path = os.path.join(path, f"{name}_normald{ext}")
            elif "color" in file.lower():
                new_file_path = os.path.join(path, f"{name}_color{ext}")
            elif "ambientocclusion" in file.lower() or "_ao" in file.lower():
                new_file_path = os.path.join(path, f"{name}_ambientocclusion{ext}")
            else:
                new_file_path = os.path.join(path, f"{name}{ext}")
            if file_path != new_file_path:
                shutil.move(file_path, new_file_path)

    def build_material(self, *args):
        if self.output_path == "" or not os.path.exists(self.output_path):
            cmds.inViewMessage(amg=f"Output path '{self.output_path}' missing or invalid", pos='midCenter', fade=True)
            return
        if self.input_path == "" or not os.path.exists(self.input_path):
            cmds.inViewMessage(amg=f"Input path '{self.input_path}' missing or invalid", pos='midCenter', fade=True)
            return

        cmds.text(self.lbl_status_update, edit=True, label="Started build")

        if self.is_zip:
            self.unzip(self.zip_input_path, self.output_path)
        else:
            if not os.path.exists(self.output_path):
                os.mkdir(self.output_path)

            for file in os.listdir(self.input_path):
                if os.path.splitext(file)[0] == ".mayaSwatches":
                    continue
                file_path = os.path.join(self.input_path, file)
                new_file_path = os.path.join(self.output_path, file)
                if file_path != new_file_path:
                    shutil.copy(file_path, new_file_path)
            self.rename_inside_dir(self.output_path)

        BuildMaterial(self.output_path, self.lbl_status_update)

    def build_material_window(self):
        if cmds.window("buildMaterialWindow", exists=True):
            cmds.deleteUI("buildMaterialWindow", window=True)

        width, height = 600, 300
        self.window = cmds.window("buildMaterialWindow", title="Build Material", widthHeight=(width, height), sizeable=False)
        self.lyt_grid = cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(width/2, 50), parent=self.window)

        cmds.button(label="Select Material Folder", command=self.open_folder_selector_dialog, parent=self.lyt_grid)
        self.lbl_folder = cmds.text(label="Folder path", parent=self.lyt_grid)

        cmds.button(label="Or Select Material ZIP", command=self.open_zip_selector_dialog, parent=self.lyt_grid)
        self.lbl_zip = cmds.text(label="Zip path", parent=self.lyt_grid)

        cmds.button(label="Select output folder", command=self.open_output_folder_selector_dialog, parent=self.lyt_grid)
        self.lbl_output_path = cmds.text(label="Output path", parent=self.lyt_grid)

        cmds.button(label="Build", command=self.build_material, parent=self.lyt_grid)
        self.lbl_status_update = cmds.text(label="", parent=self.lyt_grid)

        cmds.showWindow(self.window)
