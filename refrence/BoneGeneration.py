import bpy

#Create armature and armature object
armature = bpy.data.armatures.new('Armature')
armature_object = bpy.data.objects.new('Armature', armature)
#Link armature object to our scene
bpy.context.scene.objects.link(armature_object)

#Make a coding shortcut 
armature_data = bpy.data.objects['Armature']

#Must make armature active and in edit mode to create a bone
bpy.context.scene.objects.active = armature_data
bpy.ops.object.mode_set(mode='EDIT', toggle=False)

#Make a bone
bone = armature_data.data.edit_bones.new('Bone')
bone.head = (0,0,0)
bone.tail = (0,0,1)

#Create empty mesh to use as custom bone shape
mesh = bpy.data.meshes.new('mesh')

size = (0.5588,0.9144,0.9144)
location = (0,0,0)

#Vert position XYZ in order of XnYnZn, XnYpZn, XpYnZn, XpYpZn.
verts = [
    (0,0,0), 
    (0, size[1], 0),
    (size[0], 0, 0),
    (size[0], size[1], 0)
    ]
        
#Vertex forming faces in order of Xn, Yp, Xp, Yn.
faces = [
    (0,1),
    (1,3),
    (3,2),
    (2,0)
    ]

#Create vertices and faces for mesh
mesh.from_pydata(verts, [], faces)
#bone_shape.update(calc_edges=True)

#Create bone shape from mesh
bone_shape = bpy.data.objects.new('bone_shape', mesh)
bpy.context.scene.objects.link(bone_shape)

#print(dir(pivot_bone))
print(armature_object.pose.bones)
armature_object.pose.bones['Bone'].custom_shape = bone_shape

#Exit Armature editing
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)