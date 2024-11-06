bl_info = {
    "name": "VRM-Spacing-Animation-Baking",
    "author": "ingenoire",
    "version": (1, 9),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > VRM Bake",
    "description": "Adjusts spacing for VRM bones and provides animation baking tools.",
    "category": "Animation",
}

import bpy
import math

# List of bone pairs for dropdown menu
bone_pairs = [
    ("SHOULDER", "J_Bip_L_Shoulder", "J_Bip_R_Shoulder", "Shoulder"),
    ("UPPER_ARM", "J_Bip_L_UpperArm", "J_Bip_R_UpperArm", "Upper Arm"),
    ("LOWER_ARM", "J_Bip_L_LowerArm", "J_Bip_R_LowerArm", "Lower Arm"),
    ("UPPER_LEG", "J_Bip_L_UpperLeg", "J_Bip_R_UpperLeg", "Upper Leg"),
    ("LOWER_LEG", "J_Bip_L_LowerLeg", "J_Bip_R_LowerLeg", "Lower Leg")
]

# Add a toggle property for choosing spacing axis
bpy.types.Scene.spacing_axis = bpy.props.EnumProperty(
    name="Spacing Axis",
    description="Choose which axis to apply the spacing on",
    items=[
        ('SIDEWAYS', "Space Sideways (Z-Axis)", ""),
        ('FORWARD_BACKWARD', "Space Forward/Backward (Y-Axis)", "")
    ],
    default='SIDEWAYS'
)

# Updated bone pair spacing function
def adjust_bone_pair_spacing(armature, bone_l_name, bone_r_name, space_value, affect_left, affect_right, axis):
    if not affect_left and not affect_right:
        return {'CANCELLED'}

    space_rad = math.radians(space_value)
    anim_data = armature.animation_data

    if anim_data is not None and anim_data.action is not None:
        # Ensure the final frame is included by using range with frame_range[1] + 1
        for f in range(int(anim_data.action.frame_range[0]), int(anim_data.action.frame_range[1]) + 1):
            bpy.context.scene.frame_set(f)

            # Determine which axis to adjust
            axis_index = 2 if axis == 'SIDEWAYS' else 1  # z-axis = 2, y-axis = 1

            # Adjust left bone if selected and keyframe exists
            if affect_left and bone_l_name in armature.pose.bones:
                bone_l = armature.pose.bones[bone_l_name]
                fcurve = anim_data.action.fcurves.find(data_path="pose.bones[\"{}\"].rotation_euler".format(bone_l_name), index=axis_index)
                if fcurve and any(kp.co[0] == f for kp in fcurve.keyframe_points):
                    bone_l.rotation_euler[axis_index] += space_rad
                    bone_l.keyframe_insert(data_path="rotation_euler", index=axis_index)

            # Adjust right bone if selected and keyframe exists
            if affect_right and bone_r_name in armature.pose.bones:
                bone_r = armature.pose.bones[bone_r_name]
                fcurve = anim_data.action.fcurves.find(data_path="pose.bones[\"{}\"].rotation_euler".format(bone_r_name), index=axis_index)
                if fcurve and any(kp.co[0] == f for kp in fcurve.keyframe_points):
                    bone_r.rotation_euler[axis_index] -= space_rad
                    bone_r.keyframe_insert(data_path="rotation_euler", index=axis_index)

# Update the operator to include the axis parameter
class SpacingAdjusterOperator(bpy.types.Operator):
    bl_idname = "object.adjust_spacing"
    bl_label = "Adjust Spacing"
    bl_description = "Adjusts the spacing of the selected bones according to the value chosen above."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.object
        bone_pair_key = context.scene.selected_bone_pair
        space_value = context.scene.space_value_prop

        affect_left = context.scene.affect_left_prop
        affect_right = context.scene.affect_right_prop
        spacing_axis = context.scene.spacing_axis

        if not affect_left and not affect_right:
            self.report({'WARNING'}, "You must select at least one bone (Left or Right) to adjust.")
            return {'CANCELLED'}

        # Get selected bone pair
        bone_pair = next((bp for bp in bone_pairs if bp[0] == bone_pair_key), None)
        if bone_pair:
            bone_l_name, bone_r_name = bone_pair[1], bone_pair[2]
            adjust_bone_pair_spacing(armature, bone_l_name, bone_r_name, space_value, affect_left, affect_right, spacing_axis)
        else:
            self.report({'ERROR'}, "Invalid bone pair selected.")
            return {'CANCELLED'}

        return {'FINISHED'}

# ----------------------------- Animation Helper Functions -----------------------------

# Operator to select physics bones
class SelectPhysicsBonesOperator(bpy.types.Operator):
    bl_idname = "object.select_physics_bones"
    bl_label = "Select Physics Bones"
    bl_description = "This selects all the possible physics bones that could exist on your VRM model."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.object

        # Ensure we are in Pose Mode
        if bpy.context.mode != 'POSE':
            bpy.ops.object.mode_set(mode='POSE')

        # Deselect all bones first
        bpy.ops.pose.select_all(action='DESELECT')

        # List of patterns for bone names
        patterns = ["Hair", "Bust", "Skirt", "Sleeve", "Ear", "Tail"]

        # Iterate over all bones and select those matching the patterns
        for bone in armature.pose.bones:
            bone_name = bone.name
            if any(pattern in bone_name for pattern in patterns):
                bone.bone.select = True  # Select matching bones

        return {'FINISHED'}



# Operator to delete highlighted bones from animation
class DeleteHighlightedBonesOperator(bpy.types.Operator):
    bl_idname = "object.delete_highlighted_bones"
    bl_label = "Delete Highlighted Bones from Animation"
    bl_description = "This removes the physics bones from the current animation, which is often the case when retargeting animations to the VRM model."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        armature = context.object
        anim_data = armature.animation_data

        if bpy.context.mode != 'POSE':
            self.report({'WARNING'}, "You must be in Pose Mode.")
            return {'CANCELLED'}

        if not armature.pose.bones:
            self.report({'WARNING'}, "No bones selected.")
            return {'CANCELLED'}

        if anim_data is None or anim_data.action is None:
            self.report({'WARNING'}, "No animation data found.")
            return {'CANCELLED'}

        selected_bones = [bone.name for bone in armature.pose.bones if bone.bone.select]

        if not selected_bones:
            self.report({'WARNING'}, "No bones selected.")
            return {'CANCELLED'}

        # Loop through selected bones and remove keyframes for all transformations
        for bone_name in selected_bones:
            fcurves = [fc for fc in anim_data.action.fcurves if fc.data_path.startswith(f'pose.bones["{bone_name}"]')]
            for fcurve in fcurves:
                anim_data.action.fcurves.remove(fcurve)

        return {'FINISHED'}


# Operator to toggle VRM Spring Bone Physics
class ToggleVRMSpringBonePhysicsOperator(bpy.types.Operator):
    bl_idname = "object.toggle_vrm_spring_bone_physics"
    bl_label = "Enable/Disable VRM Spring Bone Physics"
    bl_description = "Enable VRM Spring Bone Physics for baking; disable before creating looping animations."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Locate the Armature in the scene
        armature = None
        for obj in bpy.context.scene.objects:
            if obj.type == 'ARMATURE':
                armature = obj
                break
        
        if armature is None:
            self.report({'ERROR'}, "No Armature object found in the scene.")
            return {'CANCELLED'}
        
        # Set the Armature as the active object and select it
        bpy.context.view_layer.objects.active = armature
        armature.select_set(True)
        
        # Access the VRM Spring Bone settings
        try:
            # Toggle the spring bone physics status
            vrm_module = armature.data.vrm_addon_extension  # Placeholder for actual VRM property path
            enabled = not getattr(vrm_module.spring_bone1, 'enable_animation', False)
            vrm_module.spring_bone1.enable_animation = enabled
            
            # Update the scene property to reflect the toggle status
            context.scene.vrm_spring_bone_physics_enabled = enabled

            status = "enabled" if enabled else "disabled"
            self.report({'INFO'}, f"VRM Spring Bone Physics {status}.")

        except AttributeError:
            self.report({'ERROR'}, "VRM Spring Bone system not available.")
            return {'CANCELLED'}

        return {'FINISHED'}

    
class AdjustPlaybackAndBakeOperator(bpy.types.Operator):
    bl_idname = "object.adjust_playback_and_bake"
    bl_label = "Adjust Playback Range and Bake Animation"
    bl_description = "Bakes the hair physics into the animation and also changes the playback range of the scene to that of the animation. If you don't need a looping animation, this is the final step."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        armature = context.object

        # Ensure we're in Object Mode
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # Get the action
        anim_data = armature.animation_data
        if anim_data is None or anim_data.action is None:
            self.report({'ERROR'}, "No animation data found.")
            return {'CANCELLED'}

        action = anim_data.action

        # Adjust playback range's final frame to match the final frame of the current action
        final_frame = int(action.frame_range[1])
        scene.frame_end = final_frame

        # Bake Animation
        bpy.ops.object.mode_set(mode='POSE')  # Switch to Pose Mode
        bpy.ops.nla.bake(
            frame_start=1,
            frame_end=final_frame,
            bake_types={'POSE'},
            visual_keying=True,
            clear_constraints=False,
            use_current_action=True,
            only_selected=False
        )
        bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to Object Mode

        self.report({'INFO'}, f"Playback range adjusted to frame {final_frame} and animation baked.")
        return {'FINISHED'}
    
# ----------------------------- Loopify Physics Operator -----------------------------
class LoopifyPhysicsOperator(bpy.types.Operator):
    bl_idname = "object.loopify_physics"
    bl_label = "Loopify Physics"
    bl_description = "Deletes the front or back of the animation's physics and inserts the opposite side's last or first frame of physics bones, making the animation loop seamlessly. The more frame easing there is, the more frames are deleted, at the cost of less precise physics for a longer portion of the animation. This is the final step for looping animations."
    bl_options = {'REGISTER', 'UNDO'}

    # Use the frame easing defined in the scene properties
    def execute(self, context):
        armature = context.object

        # Ensure we are in Pose Mode
        if bpy.context.mode != 'POSE':
            bpy.ops.object.mode_set(mode='POSE')

        # Get the action
        anim_data = armature.animation_data
        if anim_data is None or anim_data.action is None:
            self.report({'ERROR'}, "No animation data found.")
            return {'CANCELLED'}

        action = anim_data.action
        frame_range = action.frame_range
        start_frame = int(frame_range[0])
        end_frame = int(frame_range[1])

        # Get user input for frame selection and easing value from context
        frame_selection = context.scene.frame_selection
        frame_easing = context.scene.loopify_frame_easing  # Correctly fetching frame easing from the scene property

        # Determine the copy frame and delete frame range based on user selection
        if frame_selection == 'LAST_FRAME':
            copy_frame = end_frame
            delete_range_start = start_frame
            delete_range_end = start_frame + frame_easing - 1
            paste_frame = 0
        else:  # 'FIRST_FRAME'
            copy_frame = start_frame
            delete_range_start = end_frame - frame_easing + 1
            delete_range_end = end_frame
            paste_frame = end_frame + 1

        # Log debug information
        print(f"Action Frame Range: {start_frame} to {end_frame}")
        print(f"Frame Selection: {frame_selection}")
        print(f"Frame Easing: {frame_easing}")
        print(f"Copy Frame: {copy_frame}")
        print(f"Delete Range: {delete_range_start} to {delete_range_end}")
        print(f"Paste Frame: {paste_frame}")

        # Get selected bones
        selected_bones = [bone.name for bone in armature.pose.bones if bone.bone.select]
        if not selected_bones:
            self.report({'ERROR'}, "No bones selected.")
            return {'CANCELLED'}
        print(f"Selected Bones: {selected_bones}")

        # Helper function to get F-Curves for selected bones
        def get_selected_bone_fcurves():
            fcurves = []
            for fcurve in action.fcurves:
                if any(bone_name in fcurve.data_path for bone_name in selected_bones):
                    fcurves.append(fcurve)
            return fcurves

        fcurves = get_selected_bone_fcurves()

        # Collect keyframe data to copy
        keyframe_data = {}
        for fcurve in fcurves:
            keyframe_data[fcurve] = {}
            for keyframe in fcurve.keyframe_points:
                if keyframe.co[0] == copy_frame:
                    keyframe_data[fcurve][keyframe.co[0]] = keyframe.co[1]

        # Delete keyframes within the delete range
        for fcurve in fcurves:
            for frame in range(delete_range_start, delete_range_end + 1):
                keyframes_to_remove = [kf for kf in fcurve.keyframe_points if kf.co[0] == frame]
                for keyframe in keyframes_to_remove:
                    fcurve.keyframe_points.remove(keyframe)

        # Insert keyframes at the paste position
        for fcurve in fcurves:
            for frame, value in keyframe_data[fcurve].items():
                fcurve.keyframe_points.insert(paste_frame, value, options={'FAST'})

        # Re-delete the original delete range to clear any additional frames
        for fcurve in fcurves:
            for frame in range(delete_range_start, delete_range_end + 1):
                keyframes_to_remove = [kf for kf in fcurve.keyframe_points if kf.co[0] == frame]
                for keyframe in keyframes_to_remove:
                    fcurve.keyframe_points.remove(keyframe)

        return {'FINISHED'}



# Example UI Panel code snippet for adding new controls
class SpacingPanel(bpy.types.Panel):
    bl_label = "VRM Space Anime Baking"
    bl_idname = "OBJECT_PT_spacing"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VRM Space Anime Baking'

    def draw(self, context):
        layout = self.layout

        # ------------------- Spacing Section -------------------
        layout.label(text="Bone Spacing Adjuster", icon='ARMATURE_DATA')

        row = layout.row(align=True)
        row.prop(context.scene, 'selected_bone_pair', text="Bone Pair")
        row = layout.row(align=True)
        row.prop(context.scene, 'affect_left_prop', text="Affect Left", icon='TRIA_LEFT')
        row.prop(context.scene, 'affect_right_prop', text="Affect Right", icon='TRIA_RIGHT')

        layout.prop(context.scene, 'space_value_prop', text="Spacing Value", icon='ARROW_LEFTRIGHT')

        # Add the new axis toggle
        layout.prop(context.scene, 'spacing_axis', text="Spacing Axis")

        layout.operator("object.adjust_spacing", text="Adjust Spacing", icon='MODIFIER')

        layout.separator(factor=0.5)

        # ------------------- Animation Helper Section -------------------
        layout.label(text="Animation Helper", icon='ANIM')

        row = layout.row(align=True)
        row.operator("object.select_physics_bones", text="Select Physics Bones", icon='BONE_DATA')
        row.operator("object.delete_highlighted_bones", text="Delete Highlighted Bones", icon='TRASH')

        # Toggle button for VRM spring bone physics with status indicator
        layout.separator(factor=0.5)
        is_enabled = context.scene.vrm_spring_bone_physics_enabled
        icon = 'CHECKBOX_HLT' if is_enabled else 'CHECKBOX_DEHLT'
        status_text = "VRM Spring Bone Physics ON" if is_enabled else "VRM Spring Bone Physics OFF"
        layout.operator("object.toggle_vrm_spring_bone_physics", text=status_text, icon=icon)

        layout.separator(factor=0.5)

        # Adjust Playback and Bake
        layout.operator("object.adjust_playback_and_bake", text="Adjust Playback & Bake", icon='RENDER_ANIMATION')

        # Loopify Physics
        layout.separator(factor=0.5)
        layout.prop(context.scene, "frame_selection", text="Frame Selection", icon='TIME')
        layout.prop(context.scene, "loopify_frame_easing", text="Frame Easing", icon='IPO_ELASTIC')
        layout.operator("object.loopify_physics", text="Loopify Physics", icon='CON_FOLLOWPATH')

# ----------------------------- Register/Unregister Functions -----------------------------

def register():
    bpy.utils.register_class(SpacingAdjusterOperator)
    bpy.utils.register_class(SelectPhysicsBonesOperator)
    bpy.utils.register_class(DeleteHighlightedBonesOperator)
    bpy.utils.register_class(SpacingPanel)
    bpy.utils.register_class(AdjustPlaybackAndBakeOperator)
    bpy.utils.register_class(ToggleVRMSpringBonePhysicsOperator)
    bpy.utils.register_class(LoopifyPhysicsOperator)

    bpy.types.Scene.selected_bone_pair = bpy.props.EnumProperty(
        name="Bone Pair",
        description="Select the bone pair to adjust",
        items=[(bp[0], bp[3], "") for bp in bone_pairs],
        default='SHOULDER'
    )

    bpy.types.Scene.affect_left_prop = bpy.props.BoolProperty(
        name="Affect Left",
        description="Affect the left bone",
        default=True
    )
    bpy.types.Scene.affect_right_prop = bpy.props.BoolProperty(
        name="Affect Right",
        description="Affect the right bone",
        default=True
    )
    bpy.types.Scene.space_value_prop = bpy.props.FloatProperty(
        name="Spacing Value",
        description="Spacing value in degrees",
        default=5.0,
        min=-20.0,
        max=20.0
    )
    bpy.types.Scene.spacing_axis = bpy.props.EnumProperty(
        name="Spacing Axis",
        description="Choose which axis to apply the spacing on",
        items=[
            ('SIDEWAYS', "Space Sideways (Z-Axis)", ""),
            ('FORWARD_BACKWARD', "Space Forward/Backward (Y-Axis)", "")
        ],
        default='SIDEWAYS'
    )

    bpy.types.Scene.frame_selection = bpy.props.EnumProperty(
        name="Frame Selection",
        description="Choose the frame to base the loop from",
        items=[('LAST_FRAME', "Last Frame (Recommended)", ""),
               ('FIRST_FRAME', "First Frame", "")],
        default='LAST_FRAME'
    )

    bpy.types.Scene.loopify_frame_easing = bpy.props.IntProperty(
        name="Frame Easing from Loop",
        description="Number of frames to ease out physics when looping",
        default=4
    )

    bpy.types.Scene.vrm_spring_bone_physics_enabled = bpy.props.BoolProperty(
        name="VRM Spring Bone Physics",
        description="Toggle VRM Spring Bone Physics ON/OFF",
        default=False
    )


def unregister():
    bpy.utils.unregister_class(SpacingAdjusterOperator)
    bpy.utils.unregister_class(SelectPhysicsBonesOperator)
    bpy.utils.unregister_class(DeleteHighlightedBonesOperator)
    bpy.utils.unregister_class(SpacingPanel)
    bpy.utils.unregister_class(AdjustPlaybackAndBakeOperator)
    bpy.utils.unregister_class(ToggleVRMSpringBonePhysicsOperator)
    bpy.utils.unregister_class(LoopifyPhysicsOperator)

    del bpy.types.Scene.selected_bone_pair
    del bpy.types.Scene.affect_left_prop
    del bpy.types.Scene.affect_right_prop
    del bpy.types.Scene.space_value_prop
    del bpy.types.Scene.spacing_axis
    del bpy.types.Scene.frame_selection
    del bpy.types.Scene.loopify_frame_easing
    del bpy.types.Scene.vrm_spring_bone_physics_enabled


if __name__ == "__main__":
    register()
