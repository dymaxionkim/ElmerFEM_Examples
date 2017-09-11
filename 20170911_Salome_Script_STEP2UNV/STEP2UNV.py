# -*- coding: utf-8 -*-

#################################################
#
#   STEP2UNV for Elmer with Salome
#   V01
#
#   Data: 2017-09-11
#   Modifier : DymaxionKim
#
#   - Salome 8.2
#   - Import single STEP assembly file
#   - Excecute in CUI but not Salome GUI
#   - Only for STEP format
#   - Auto Group for each solids, subshape faces, intersect faces
#
#################################################

import sys
import salome
import os

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)


"""
#################################################
## User Inputs
#################################################
# WORKING DIRECTORY
#print("\n" * 100)
DIRECTORY = raw_input("Input your working directory path : ")
print("Working directory path : ", DIRECTORY)
sys.path.insert( 0, DIRECTORY)

# File Name
FILENAME = raw_input("Input your STEP File Name : ")
print("STEP File Name : ", FILENAME)

# Mesh Parameters
MaxMeshSize = 10.0   # specify in mm
MinMeshSize = 2.0   # specify in mm
MeshSegPerEdge = 10
MeshGrowthRate = 0.7

print("Hypothesys for NETGEN")
MaxMeshSize = float(raw_input("MaxMeshSize[mm] : "))
MinMeshSize = float(raw_input("MinMeshSize[mm] : "))
MeshSegPerEdge = float(raw_input("MeshSegPerEdge[ea] : "))
MeshGrowthRate = float(raw_input("MeshGrowthRate[0~1] : "))
"""

## temp
DIRECTORY = "/home/osboxes/.config/salome/cad_import/test"
FILENAME = "aaa.step"
sys.path.insert( 0, DIRECTORY)
MaxMeshSize = 10
MinMeshSize = 2.0
MeshSegPerEdge = 10
MeshGrowthRate = 0.3


#################################################
### GEOM component
#################################################
import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


# New Study
geompy = geomBuilder.New(theStudy)

# Read STEP File
PARTS = []
ASSEMBLY = geompy.ImportSTEP(DIRECTORY+"/"+FILENAME, False, True)
PARTS = geompy.ExtractShapes(ASSEMBLY, geompy.ShapeType["SOLID"], True)
PARTITION = geompy.MakePartition(PARTS, [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
PARTS = geompy.ExtractShapes(PARTITION, geompy.ShapeType["SOLID"], True)


#################################################
# GROUP (VOLUMES of PARTS)
#################################################
GROUP_PARTS = []
ID_PARTS = []
for aPART in range(0,len(PARTS)):
	ID_PARTS.append(geompy.GetSubShapeID(PARTITION, PARTS[aPART]))
for aGROUP in range(0,len(PARTS)):
	GROUP_PARTS.append(geompy.CreateGroup(PARTITION, geompy.ShapeType["SOLID"]))
for aGROUP in range(0,len(PARTS)):
	geompy.AddObject(GROUP_PARTS[aGROUP], ID_PARTS[aGROUP])

# Add to Study
geompy.addToStudy( PARTITION, 'PARTITION' )
for aGROUP in range(0,len(GROUP_PARTS)):
	geompy.addToStudyInFather(PARTITION, GROUP_PARTS[aGROUP], 'PART{0}'.format(aGROUP+1) )


#################################################
# GROUP (FACES of PARTS)
#################################################
GROUP_FACES = []
for aGROUP in range(0,len(GROUP_PARTS)):
	FACES = []
	ID_FACES = []
	FACES = geompy.SubShapeAll(GROUP_PARTS[aGROUP], geompy.ShapeType["FACE"])
	for fGROUP in range(0,len(FACES)):
		ID_FACES.append(geompy.GetSubShapeID(PARTITION, FACES[fGROUP]))
	GROUP_FACES.append(geompy.CreateGroup(PARTITION, geompy.ShapeType["FACE"]))
	geompy.UnionIDs(GROUP_FACES[aGROUP], ID_FACES)

# Add to Study
for aGROUP in range(0,len(GROUP_PARTS)):
	geompy.addToStudyInFather(PARTITION, GROUP_FACES[aGROUP], 'FACE{0}'.format(aGROUP+1) )


#################################################
# GROUP (INTERSECT FACES of PARTS)
#################################################
GROUP_INTERSECTS = []
for fGROUP in range(0,len(GROUP_FACES)):
	for fGROUP2 in range(fGROUP+1,len(GROUP_FACES)):
		if fGROUP!=fGROUP2:
			GROUP_INTERSECTS.append( geompy.IntersectListOfGroups([GROUP_FACES[fGROUP], GROUP_FACES[fGROUP2]]) )

# Add to Study
for iGROUP in range(0,len(GROUP_INTERSECTS)):
	geompy.addToStudyInFather(PARTITION, GROUP_INTERSECTS[iGROUP], 'INTERSECT{0}'.format(iGROUP+1) )


#################################################
# GROUP (CUT FACES of PARTS)
#################################################
#Cut_1 = geompy.CutListOfGroups([Group_4], [Intersect_1])


#################################################
### SMESH component
#################################################
import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

# New Study
smesh = smeshBuilder.New(theStudy)

# New Mesh
MESH = smesh.Mesh(PARTITION)

# Parameters (temp)
MaxMeshSize = 10.0   # specify in mm
MinMeshSize = 2.0   # specify in mm
MeshSegPerEdge = 10
MeshGrowthRate = 0.7

# Parameters
NETGEN_2D3D = MESH.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_Parameters = NETGEN_2D3D.Parameters()
NETGEN_Parameters.SetMaxSize( MaxMeshSize*0.001 )
NETGEN_Parameters.SetMinSize( MinMeshSize*0.001 )
NETGEN_Parameters.SetSecondOrder( 1 )
# SetFiness ::: 0=VeryCoarse, 1=Coarse, 2=Moderate, 3=Fine, 4=VeryFine, 5=Custom
NETGEN_Parameters.SetFineness( 5 )
NETGEN_Parameters.SetGrowthRate( MeshGrowthRate )
NETGEN_Parameters.SetNbSegPerEdge( MeshSegPerEdge )
NETGEN_Parameters.SetNbSegPerRadius( 2 )
NETGEN_Parameters.SetUseSurfaceCurvature( 1 ) # 0 or 1
NETGEN_Parameters.SetQuadAllowed( 0 )
NETGEN_Parameters.SetOptimize( 1 )
NETGEN_Parameters.SetFuseEdges( 1 )


#################################################
# GROUP (VOLUMES of PARTS)
#################################################
MGROUP_PARTS = []
for aGROUP in range(0,len(GROUP_PARTS)):
	MGROUP_PARTS.append( MESH.GroupOnGeom(GROUP_PARTS[aGROUP], 'PART{0}'.format(aGROUP+1), SMESH.VOLUME) )


#################################################
# GROUP (FACES of PARTS)
#################################################
MGROUP_FACES = []
for aGROUP in range(0,len(GROUP_PARTS)):
	MGROUP_FACES.append( MESH.GroupOnGeom(GROUP_FACES[aGROUP], 'FACE{0}'.format(aGROUP+1), SMESH.FACE) )

MGROUP_INTERSECTS = []
for iGROUP in range(0,len(GROUP_INTERSECTS)):
	MGROUP_INTERSECTS.append( MESH.GroupOnGeom(GROUP_INTERSECTS[iGROUP], 'INTERSECT{0}'.format(iGROUP+1), SMESH.FACE) )

#################################################
# Make MESH
#################################################
isDone = MESH.Compute()


#################################################
# Make UNV
#################################################
FILENAME_HEAD = os.path.splitext(FILENAME)[-2]
try:
  MESH.ExportUNV( DIRECTORY+"/"+FILENAME_HEAD+".unv")
except:
  print 'ExportUNV() failed. Invalid file name?'


#################################################
# DISPLAY
#################################################
#if salome.sg.hasDesktop():
#  salome.sg.updateObjBrowser(True)


