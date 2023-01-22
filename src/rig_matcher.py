import bpy
import os

context = bpy.context
scene = context.scene

copy_from_armature = context.active_object
copy_to_armature   = context.selected_objects[0]

def Perform():
    # bpy.ops.object.select_all(action='DESELECT')
    copy_from_armature.select_set(True)
    context.view_layer.objects.active = copy_from_armature
    
    # Put us into object mode and store the bone configurations from our copy_from armature
    bpy.ops.object.mode_set(mode='EDIT')

    bone_store = {}
    for bone in copy_from_armature.data.edit_bones[:]:
        store = {
            'name': bone.name,
            'head': bone.head.copy(),
            'tail': bone.tail.copy(),
            'roll': bone.roll,
            'head_radius': bone.head_radius,
            'tail_radius': bone.tail_radius,
            'envelope_weight': bone.envelope_weight
        }
        
        bone_store[bone.name] = store

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    copy_to_armature.select_set(True)
    context.view_layer.objects.active = copy_to_armature
    bpy.ops.object.mode_set(mode='EDIT')
    
    for copy_bone_name in bone_store:
        copy_bone = bone_store[copy_bone_name]
        to_bones = copy_to_armature.data.edit_bones
        to_bone = None
        
        if copy_bone_name in to_bones:
            to_bone = to_bones[copy_bone_name]
        else:
            continue
            to_bone = to_bones.new(copy_bone_name)
            
        to_bone.head 	  	 	= copy_bone['head']
        to_bone.tail 	  	 	= copy_bone['tail']
        to_bone.roll 	  	 	= copy_bone['roll']
        to_bone.head_radius 	= copy_bone['head_radius']
        to_bone.tail_radius 	= copy_bone['tail_radius']
        to_bone.envelope_weight = copy_bone['envelope_weight']



if len(context.selected_objects) == 2 and copy_from_armature is not None and copy_to_armature is not None and copy_from_armature.type == 'ARMATURE' and copy_to_armature.type == 'ARMATURE':
    from os import system
    Perform()
else:
    print("You must select two objects; they both must be armatures.")