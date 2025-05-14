import os
import maya.cmds as cmds
import maya.api.OpenMaya as om

class BuildMaterial(om.MPxCommand):
    kPluginCmdName = "buildMaterial"

    @staticmethod
    def cmdCreator():
        return BuildMaterial(None, None)

    def run(self):
        pass

    def __init__(self, input_dir, status_update):
        om.MPxCommand.__init__(self)
        self.input_dir = input_dir
        self.status_update = status_update

        DISPLACEMENT = None
        ROUGHNESS = None
        NORMAL_GL = None
        COLOR = None
        AMBIENT_OCC = None
        MAT_NAME = os.path.basename(input_dir)

        for file in os.listdir(input_dir):
            if "displacement" in file.lower():
                DISPLACEMENT = file
            elif "roughness" in file.lower():
                ROUGHNESS = file
            elif "normalgl" in file.lower():
                NORMAL_GL = file
            elif "color" in file.lower():
                COLOR = file
            elif "ambientocclusion" in file.lower() or "_ao" in file.lower():
                AMBIENT_OCC = file

        """ Abort if crucial files are missing """
        if DISPLACEMENT == None:
            cmds.inViewMessage(amg=f"Displacement file missing. Aborting", pos='midCenter', fade=True)
            return
        if ROUGHNESS == None:
            cmds.inViewMessage(amg=f"Roughness file missing. Aborting", pos='midCenter', fade=True)
            return
        if NORMAL_GL == None:
            cmds.inViewMessage(amg=f"Normal_gl file missing. Aborting", pos='midCenter', fade=True)
            return
        if COLOR == None:
            cmds.inViewMessage(amg=f"Color file missing. Aborting", pos='midCenter', fade=True)
            return

        """ TODO: try to remove the input_dir so it uses relative file paths """
        displacement_path = os.path.join(input_dir, DISPLACEMENT)
        roughness_path = os.path.join(input_dir, ROUGHNESS)
        normal_gl_path = os.path.join(input_dir, NORMAL_GL)
        color_path = os.path.join(input_dir, COLOR)
        if AMBIENT_OCC != None:
            ambient_occ_path = os.path.join(input_dir, AMBIENT_OCC)
        export_path = os.path.join(input_dir, MAT_NAME+".ma")

        ambient_occ_file_n = None

        nodes = []

        cmds.text(status_update, edit=True, label="Building material")
        place_2d_texture_n = cmds.shadingNode('place2dTexture', asUtility=True, name=f'{MAT_NAME}_place2dTexture')
        nodes.append(place_2d_texture_n)

        displacement_file_n = cmds.shadingNode('file', asTexture=True, name=DISPLACEMENT)
        nodes.append(displacement_file_n)
        cmds.setAttr(displacement_file_n + '.fileTextureName', displacement_path, type="string")
        cmds.setAttr(displacement_file_n + '.colorSpace', 'Raw', type='string')
        cmds.setAttr(displacement_file_n + '.alphaIsLuminance', 1)
        cmds.setAttr(displacement_file_n + '.alphaOffset', -0.5)
        cmds.connectAttr(place_2d_texture_n + '.outUV', displacement_file_n + '.uvCoord', force=True)


        color_file_n = cmds.shadingNode('file', asTexture=True, name=COLOR)
        nodes.append(color_file_n)
        cmds.setAttr(color_file_n + '.fileTextureName', color_path, type="string")
        cmds.connectAttr(place_2d_texture_n + '.outUV', color_file_n + '.uvCoord', force=True)

        ambient_occ_file_n = None
        if AMBIENT_OCC != None:
            ambient_occ_file_n = cmds.shadingNode('file', asTexture=True, name=AMBIENT_OCC)
            nodes.append(ambient_occ_file_n)
            cmds.setAttr(ambient_occ_file_n + '.fileTextureName', ambient_occ_path, type="string")
            cmds.connectAttr(place_2d_texture_n + '.outUV', ambient_occ_file_n + '.uvCoord', force=True)


        roughness_file_n = cmds.shadingNode('file', asTexture=True, name=ROUGHNESS)
        nodes.append(roughness_file_n)
        cmds.setAttr(roughness_file_n + '.fileTextureName', roughness_path, type="string")
        cmds.setAttr(roughness_file_n + '.colorSpace', 'Raw', type='string')
        cmds.setAttr(roughness_file_n + '.alphaIsLuminance', 1)
        cmds.connectAttr(place_2d_texture_n + '.outUV', roughness_file_n + '.uvCoord', force=True)

        normal_gl_file_n = cmds.shadingNode('file', asTexture=True, name=NORMAL_GL)
        nodes.append(normal_gl_file_n)
        cmds.setAttr(normal_gl_file_n + '.fileTextureName', normal_gl_path, type="string")
        cmds.setAttr(normal_gl_file_n + '.colorSpace', 'Raw', type='string')
        cmds.setAttr(normal_gl_file_n + '.alphaIsLuminance', 1)
        cmds.connectAttr(place_2d_texture_n + '.outUV', normal_gl_file_n + '.uvCoord', force=True)

        place_2d_texture_attributes = [
            "coverage",
            "mirrorU",
            "mirrorV",
            "noiseUV",
            "offset",
            "outUvFilterSize",
            "repeatUV",
            "rotateFrame",
            "rotateUV",
            "stagger",
            "translateFrame",
            "vertexCameraOne",
            "vertexUvOne",
            "vertexUvThree",
            "vertexUvTwo",
            "wrapU",
            "wrapV"
        ]

        for attr in place_2d_texture_attributes:
            try:
                cmds.connectAttr(f"{place_2d_texture_n}.{attr}", f"{displacement_file_n}.{attr}", force=True)
                cmds.connectAttr(f"{place_2d_texture_n}.{attr}", f"{roughness_file_n}.{attr}", force=True)
                cmds.connectAttr(f"{place_2d_texture_n}.{attr}", f"{normal_gl_file_n}.{attr}", force=True)
                cmds.connectAttr(f"{place_2d_texture_n}.{attr}", f"{color_file_n}.{attr}", force=True)
                cmds.connectAttr(f"{place_2d_texture_n}.{attr}", f"{ambient_occ_file_n}.{attr}", force=True)
            except:
                pass

        displacement_shader_n = cmds.shadingNode('displacementShader', asShader=True, name=f'{MAT_NAME}_displacementShader')
        nodes.append(displacement_shader_n)
        cmds.connectAttr(displacement_file_n + '.outAlpha', displacement_shader_n + '.displacement', force=True)

        shading_group_n = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{MAT_NAME}_myShaderSG')
        nodes.append(shading_group_n)
        cmds.connectAttr(displacement_shader_n + '.displacement', shading_group_n + '.displacementShader', force=True)

        bump_2d_n = cmds.shadingNode('bump2d', asShader=True, name=f'{MAT_NAME}_bump2d')
        nodes.append(bump_2d_n)
        cmds.connectAttr(normal_gl_file_n + '.outAlpha', bump_2d_n + '.bumpValue', force=True)
        cmds.setAttr(bump_2d_n + '.bumpInterp', 1)

        ai_standard_surface_n = cmds.shadingNode('aiStandardSurface', asShader=True, name=f'{MAT_NAME}')
        nodes.append(ai_standard_surface_n)
        cmds.setAttr(ai_standard_surface_n + '.emission', 1.0)
        cmds.setAttr(ai_standard_surface_n + '.emissionColor', 0, 0, 0, type='double3')

        if AMBIENT_OCC != None:
            ai_multiply_n = cmds.shadingNode('aiMultiply', asShader=True, name=f'{MAT_NAME}_aiMultiply')
            nodes.append(ai_multiply_n)
            cmds.connectAttr(color_file_n + '.outColor', ai_multiply_n + '.input1', force=True)
            cmds.connectAttr(ambient_occ_file_n + '.outColor', ai_multiply_n + '.input2', force=True)
            cmds.connectAttr(ai_multiply_n + '.outColor', ai_standard_surface_n + '.baseColor', force=True)
        else:
            cmds.connectAttr(color_file_n + '.outColor', ai_standard_surface_n + '.baseColor', force=True)
        cmds.connectAttr(roughness_file_n + '.outAlpha', ai_standard_surface_n + '.specularRoughness', force=True)
        cmds.connectAttr(bump_2d_n + '.outNormal', ai_standard_surface_n + '.normalCamera', force=True)

        cmds.connectAttr(ai_standard_surface_n + '.outColor', shading_group_n + '.surfaceShader', force=True)
        if nodes:
            cmds.select(nodes, r=True)
            print(f"Selected nodes: {nodes}")
            cmds.text(status_update, edit=True, label="Exprting ma")
            cmds.file(export_path, force=True, options="v=0", type="mayaAscii", exportSelected=True)

        else:
            cmds.inViewMessage(amg=f"Something went wrong when exportin material (.ma)", pos='midCenter', fade=True)
        cmds.text(status_update, edit=True, label="Build complete")
