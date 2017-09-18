# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v8.2.0 with dump python functionality
###

import sys
import salome
import os

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/osboxes/github/ElmerFEM_Examples/20170902_Salome_Script_cad_import/example')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New(theStudy)

#################################################
## READ STEP files
#################################################
path = "/home/osboxes/github/ElmerFEM_Examples/20170902_Salome_Script_cad_import/example"
parts = []
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
for ext in ListSTEP:
	parts.append(geompy.Import(path+"/"+ext,"STEP"))

#################################################
## PARTITION
#################################################
if (len(parts) < 2):
	msg = "This script is made for multiple bodies. cannot continue"
	print msg

p1 = geompy.MakePartition(parts,[],[],[],geompy.ShapeType["SOLID"], 0, [], 0)

 # GetObjectIDs
p1_solids = geompy.ExtractShapes(p1, geompy.ShapeType["SOLID"],False)
msg = "Solids read in: {0} - Solids in model: {1}\n".format(len(parts),len(p1_solids))
print msg

if (len(p1_solids) > len(parts)):
	msg = "Wrong number of solids! Check for partly intersecting objects and for hollow objects"
	print msg

#################################################
## GROUP (SOLID)
#################################################
# Get ID (solid)
id_p1_solids = [] #initialize the array
for aSolid in range(0,len(p1_solids)):
	id_p1_solids.append(geompy.GetSubShapeID(p1, p1_solids[aSolid])) #get the ID of the solid and add it to the array

# make groups (solid)
g = []
for aGroup in range(0,len(p1_solids)):
   g.append(geompy.CreateGroup(p1, geompy.ShapeType["SOLID"]))
for aGroup in range(0,len(p1_solids)):
	geompy.AddObject(g[aGroup], id_p1_solids[aGroup])

# add objects in the study
id_p1 = geompy.addToStudy(p1,"p1")
for aGroup in range(0,len(p1_solids)):
	geompy.addToStudyInFather(p1, g[aGroup], 'body{0}'.format(aGroup+1) )

#################################################
## GROUP (SURFACE)
#################################################
for aSolid in range(0,len(p1_solids)):
	# Get ID (surface)
	p1_sufaces = geompy.ExtractShapes(p1_solids[aSolid], geompy.ShapeType["FACE"],False)
	id_p1_sufaces = []
	for aSurface in range(0,len(p1_solids)):
		id_p1_sufaces.append(geompy.GetSubShapeID(p1, p1_sufaces[aSurface]))
	# make groups (surface)
	gf = []
	for aGroup in range(0,len(p1_sufaces)):
	   gf.append(geompy.CreateGroup(p1, geompy.ShapeType["FACE"]))
	for aGroup in range(0,len(p1_sufaces)):
		geompy.AddObject(gf[aGroup], id_p1_sufaces[aGroup])
	geompy.UnionIDs(gf[aGroup], id_p1_sufaces)
	# add objects in the study
	for aGroup in range(0,len(p1_sufaces)):
		geompy.addToStudyInFather(p1, gf[aGroup], 'face{0}'.format(aGroup+1) )

#Intersect_1 = geompy.IntersectListOfGroups([Group_4, Group_5])
#Cut_1 = geompy.CutListOfGroups([Group_4], [Intersect_1])
#Cut_2 = geompy.CutListOfGroups([Group_5], [Intersect_1])


###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh_1 = smesh.Mesh(p1)
NETGEN_2D3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)

NETGEN_3D_Parameters_1 = NETGEN_2D3D.Parameters()
NETGEN_3D_Parameters_1.SetMaxSize( 0.002 )
NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
NETGEN_3D_Parameters_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1.SetMinSize( 0.0001 )
NETGEN_3D_Parameters_1.SetNbSegPerEdge(10)
NETGEN_3D_Parameters_1.SetNbSegPerRadius(10)
NETGEN_3D_Parameters_1.SetGrowthRate(0.3)
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )

##### Compute
isDone = Mesh_1.Compute()

##### Group
for aGroup in range(0,len(p1_solids)):
    NETGEN_3D_Parameters_1.GroupOnGeom(g[aGroup],'body{0}'.format(aGroup+1),SMESH.VOLUME)

for aSolid in range(0,len(p1_solids)):
	p1_sufaces = geompy.ExtractShapes(p1_solids[aSolid], geompy.ShapeType["FACE"],False)
	gf = []
	for aGroup in range(0,len(p1_sufaces)):
		NETGEN_3D_Parameters_1.GroupOnGeom(gf[aGroup],'face{0}'.format(aGroup+1),SMESH.FACE)



if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
