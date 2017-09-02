# -----------------------------------------------------------------------------------------
#
#   salome multibody CAD import for elmer
#
#   Copyright 2012, Rainer Ochs
#   initially based on a macro from madstamm (AWG20)
#
#	Data: 2012-11-15
#	Author: Rainer Ochs
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#   Permission to use this software for any purpose and without fee is hereby granted
#   If you distribute this software you have to include this copyright notice in all copies.
#
#   Description
#   This macro will read in CAD geometry into salome and mesh it.
#   Bodies and are grouped and the mesh is exported to mesh.unv in the same directory
#   The index of bodies can be controlled by the order of import.
#--------------------------------------------------------------------------------------------
#
#   Modified salome multibody CAD import for elmer
#   V01
#
#   Fork from : http://www.elmerfem.org/forum/viewtopic.php?f=9&t=2738
#   Data: 2017-09-02
#   Modifier : DymaxionKim
#
#   - Some Functions for User Input
#   - Excecute in CUI but not Salome GUI
#   - Only for STEP format
#   - Each parts should be separated files
#
#   Ref.
#    Search specific files : https://wikidocs.net/39
#
#--------------------------------------------------------------------------------------------

import geompy
import salome
import os
#gg = salome.ImportComponentGUI("GEOM")

parts = []

error = 0

tolerance = 0.00001	# max tolerance for identification of vertices


#################################################
## SECTION TO EDIT
#################################################

# Working directory
path = raw_input("Input your working directory path : ")
print("#################################################")
print("Working directory path : ", path)

# PartName
def search_STEP(dirname):
	filenames = os.listdir(dirname)
	ext2 = []
	for filename in filenames:
		ext = os.path.splitext(filename)[-1]
		if ext == '.step':
			ext2.append(filename)
	return ext2

ListSTEP = search_STEP(path)
print("#################################################")
print("List of STEP files...")
print(ListSTEP)

# add here the bodies. Each file shall only contain one body or one "solid"
# Bodies that contain other bodies shall be at the end.
# If this is respected the order of import represents the body index in the mesh

# Read STEP files
for ext in ListSTEP:
	parts.append(geompy.ImportFile(path+"/"+ext,"STEP"))

# Hypothesys for NETGEN
MinMeshSize = 2.0   # specify in mm
MaxMeshSize = 10.0   # specify in mm
MeshSegPerEdge = 10
MeshOptimize = 1	# 1 for optimize, 0 for no optimization
MeshGrowthRate = 0.7
print("#################################################")
print("Hypothesys for NETGEN")
MinMeshSize = float(raw_input("MinMeshSize[mm] : "))
MaxMeshSize = float(raw_input("MaxMeshSize[mm] : "))
MeshSegPerEdge = float(raw_input("MeshSegPerEdge[ea] : "))
MeshGrowthRate = float(raw_input("MeshGrowthRate[0~1] : "))

#################################################
## END SECTION TO EDIT
#################################################

# make partition
if (len(parts) < 2):
	msg = "This script is made for multiple bodies. cannot continue"
	print msg

p1 = geompy.MakePartition(parts,[],[],[],geompy.ShapeType["SOLID"], 0, [], 0)
 # GetObjectIDs
p1_solids = geompy.ExtractShapes(p1, geompy.ShapeType["SOLID"],False) #gets all solids in partition
msg = "Solids read in: {0} - Solids in model: {1}\n".format(len(parts),len(p1_solids))
print msg

if (len(p1_solids) > len(parts)):
	msg = "Wrong number of solids! Check for partly intersecting objects and for hollow objects"
	print msg

id_p1_solids = [] #initialize the array
for aSolid in range(0,len(p1_solids)):
	id_p1_solids.append(geompy.GetSubShapeID(p1, p1_solids[aSolid])) #get the ID of the solid and add it to the array

# make groups
g = []
for aGroup in range(0,len(p1_solids)):
   g.append(geompy.CreateGroup(p1, geompy.ShapeType["SOLID"]))
for aGroup in range(0,len(p1_solids)):
	geompy.AddObject(g[aGroup], id_p1_solids[aGroup])

# add objects in the study
id_p1 = geompy.addToStudy(p1,"Part1")
for aGroup in range(0,len(p1_solids)):
	geompy.addToStudyInFather(p1, g[aGroup], 'body{0}'.format(aGroup+1) )

# display
#gg.createAndDisplayGO(id_p1)
#gg.setDisplayMode(id_p1,1)
#gg.setColor(id_p1, 150, 150, 180)
#gg.setTransparency(id_p1, 0.8)


# -------------- meshing -----------------------------------------------

import smesh, SMESH, SALOMEDS
print "meshing..."
# create a mesh
tetraN = smesh.Mesh(p1, "Mesh_1")

# create a Netgen_2D3D algorithm for solids
algo3D = tetraN.Tetrahedron(smesh.FULL_NETGEN)


# define hypotheses
n23_params = algo3D.Parameters()

#START MESH PARAM SECTION
n23_params.SetMaxSize(MaxMeshSize/1000) # here specify in m
n23_params.SetMinSize(MinMeshSize/1000)
n23_params.SetNbSegPerEdge(MeshSegPerEdge)
n23_params.SetGrowthRate(MeshGrowthRate)
n23_params.SetOptimize(MeshOptimize)
#END MESH PARAM SECTION

# compute the mesh
tetraN.Compute()
smesh.SetName(tetraN.GetMesh(), 'Mesh_1')

print "creating mesh groups"
# create mesh groups
# Sequence defines body and face index in elmer.
for aGroup in range(0,len(p1_solids)):
    tetraN.GroupOnGeom(g[aGroup],'body{0}'.format(aGroup+1),SMESH.VOLUME)

print "saving file..."
MeshFileName = path+"/"+"Mesh.unv"
tetraN.ExportUNV(MeshFileName, None )

print("#################################################")

def search_UNV(dirname):
	filenames = os.listdir(dirname)
	ext2 = []
	for filename in filenames:
		ext = os.path.splitext(filename)[-1]
		if ext == '.unv':
			print(filename)

search_UNV(path)

print("#################################################")
print("Finished!")

