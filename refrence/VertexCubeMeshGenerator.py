import bpy
import scaleConverter

#Values are in inches
x,y,z = (1,4,3)

#Convert inches to Metric
x,y,z = scaleConverter.ImperialToMetric([x,y,z])
#Define cube vertex and face data
#verts = LowerBackLeft, LowerBackRight, LowerFrontLeft, LowerFrontRight
verts = [(0,0,0),(x,0,0),(0,y,0),(x,y,0),(0,0,z),(x,0,z),(0,y,z),(x,y,z)]
#Faces = BotomVerts, TopVerts, FrontVerts, BackVerts, LeftVerts, RightVerts
faces = [(0,1,3,2),(4,5,7,6),(2,3,7,6),(0,1,5,4),(0,2,6,4),(1,3,7,5)]


#Define mesh and object
mesh = bpy.data.meshes.new("floor")
object = bpy.data.objects.new("floor", mesh)
#Set location and scene of object
object.location = (0,0,0)
bpy.context.scene.objects.link(object)
#Create mesh
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)
object.select = False

     