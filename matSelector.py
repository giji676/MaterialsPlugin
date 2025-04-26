import os
import maya.cmds as cmds
import maya.api.OpenMaya as om

class MatSelector(om.MPxCommand):
    kPluginCmdName = "matSelector"

    def __init__(self):
        om.MPxCommand.__init__(self)
        self.matSelector_last_folder = "matSelector_last_folder"
        self.lib_path = ""

        self.width, self.height = 400, 500

        self.window = None
        self.lyt_scroll = None
        self.inp_search_field = None
        self.lyt_grid = None

        self.mat_list = {}
        self.sorted_mats = []

    @staticmethod
    def cmdCreator():
        return MatSelector()

    def run(self):
        self.lib_path = self.load_last_path()
        self.open_mat_selector()
        self.refresh_directory()

    def refresh_directory(self, *args):
        self.update_mat_list()
        search_text = cmds.textField(self.inp_search_field, query=True, text=True).lower()
        if search_text != "":
            self.search()
        else:
            self.sort_mats()
        self.display_mats()

    def save_last_path(self, path):
        cmds.optionVar(stringValue=(self.matSelector_last_folder, path))

    def load_last_path(self):
        if cmds.optionVar(exists=self.matSelector_last_folder):
            last_folder = cmds.optionVar(q=self.matSelector_last_folder)
            return last_folder
        else:
            return ""

    def open_folder_selector_dialog(self, *args):
        selected = cmds.fileDialog2(
            caption="Select Material Folder",
            fileMode=2,  # 2 = Select only folder
            okCaption="Select"
        )
        if selected:
            self.lib_path = selected[0]
            self.save_last_path(self.lib_path)
            self.update_mat_list()
            self.sort_mats()
            self.display_mats()

    def search(self, *args):
        search_text = cmds.textField(self.inp_search_field, query=True, text=True).lower()

        matching_materials = []
        non_matching_materials = []
        for base_name in sorted(self.mat_list):
            if base_name.lower().startswith(search_text):
                matching_materials.append(base_name)
            else:
                non_matching_materials.append(base_name)

        self.sorted_mats = matching_materials + non_matching_materials
        self.display_mats()

    def sort_mats(self):
        self.sorted_mats = []
        for base_name in sorted(self.mat_list):
            self.sorted_mats.append(base_name)

    def update_mat_list(self):
        if not os.path.exists(self.lib_path):
            cmds.inViewMessage(amg=f"Folder '{self.lib_path}' missing", pos='midCenter', fade=True)
            return

        self.mat_list = {}
        for mat in os.listdir(self.lib_path):
            full_path = os.path.join(self.lib_path, mat)
            if os.path.isdir(full_path):
                self.load_mat(mat)

    def load_mat(self, mat):
        full_mat_path = os.path.join(self.lib_path, mat)
        if not os.path.exists(full_mat_path):
            cmds.inViewMessage(amg=f"Missing '{full_mat_path}'. Ignoring", pos='midCenter', fade=True)
            return
        ma_path = os.path.join(self.lib_path, mat, mat+".ma")
        if not os.path.exists(ma_path):
            cmds.inViewMessage(amg=f"Missing '{ma_path}'. Ignoring", pos='midCenter', fade=True)
            return
        prev_path = os.path.join(self.lib_path, mat, mat+".png")
        if not os.path.exists(ma_path):
            cmds.inViewMessage(amg=f"Missing '{prev_path}'", pos='midCenter', fade=True)

        self.mat_list[mat] = {"ma_path": ma_path, "prev_path": prev_path}

    def open_mat(self, mat_path):
        cmds.file(mat_path, i=True, ignoreVersion=True)

    def display_mats(self):
        columns = 4
        cell_width = (self.width-5*2)/columns # include 5px padding on both sides
        cell_height = cell_width + 30

        if cmds.layout("grid", exists=True):
            cmds.deleteUI("grid")

        self.lyt_grid = cmds.gridLayout("grid", numberOfColumns=columns, cellWidth=cell_width, cellHeight=cell_height, parent=self.lyt_scroll)

        for base_name in self.sorted_mats:
            cmds.columnLayout(parent=self.lyt_grid)
            cmds.iconTextButton(
                image3=self.mat_list[base_name]["prev_path"],
                style="iconOnly",
                width=cell_width,
                height=cell_width,
                command=lambda ma_path=self.mat_list[base_name]["ma_path"]: self.open_mat(ma_path),
            )
            cmds.text(label=base_name, align="center")
            cmds.setParent('..')

    def open_mat_selector(self):
        if cmds.window("materialSelectorWindow", exists=True):
            cmds.deleteUI("materialSelectorWindow", window=True)

        self.window = cmds.window("materialSelectorWindow", title="Material Selector", widthHeight=(self.width, self.height), sizeable=False)
        main_layout = cmds.formLayout(parent=self.window)
        folder_button = cmds.button(label="Select Material Lib Folder", command=self.open_folder_selector_dialog, parent=main_layout)

        row_layout = cmds.rowLayout(numberOfColumns=2, adjustableColumn=1, columnAlign=(1, 'left'), columnAttach=(2, 'both', 0), parent=main_layout)
        self.inp_search_field = cmds.textField(placeholderText="Search for material...", parent=row_layout)
        cmds.button(label="Search", command=self.search, parent=row_layout)
        btn_refresh = cmds.button(label="Refresh", command=self.refresh_directory, parent=main_layout)

        self.lyt_scroll = cmds.scrollLayout(parent=main_layout)

        cmds.formLayout(
            main_layout, edit=True,
            attachForm=[
                (folder_button, 'top', 5),
                (folder_button, 'left', 5),
                (folder_button, 'right', 5),
                (row_layout, 'left', 5),
                (row_layout, 'right', 5),
                (self.lyt_scroll, 'left', 5),
                (self.lyt_scroll, 'right', 5),
                (btn_refresh, 'left', 5),
                (btn_refresh, 'right', 5),
                (btn_refresh, 'bottom', 5)
            ],
            attachControl=[
                (row_layout, 'top', 5, folder_button),
                (self.lyt_scroll, 'top', 5, row_layout),
                (self.lyt_scroll, 'bottom', 5, btn_refresh)
            ]
        )

        cmds.showWindow(self.window)
