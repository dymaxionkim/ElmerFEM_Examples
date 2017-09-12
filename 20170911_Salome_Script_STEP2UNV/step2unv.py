# -*- coding: utf-8 -*-

#################################################
#
#   STEP2UNV for Elmer with Salome
#   V02
#
#   Data: 2017-09-12
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

#tolerance = 1e-10	# max tolerance for identification of vertices

#################################################
## User Inputs
#################################################
# WORKING DIRECTORY
#print("\n" * 100)
print("----------------------------------------------------")
print("Input your working directory :")
DIRECTORY = raw_input()
sys.path.insert( 0, DIRECTORY)

# File Name
print("----------------------------------------------------")
print("Input your STEP File Name :")
FILENAME = raw_input()

# Mesh Parameters
print("----------------------------------------------------")
print("----- Mesh Parameters -----")
MinMeshSize = float(raw_input("MinMeshSize[m] : ")) # specify in m
MaxMeshSize = float(raw_input("MaxMeshSize[m] : ")) # specify in m
#MeshSecondOrder = float(raw_input("SetSecondOrder[0,1] : "))
MeshSecondOrder = 1
print("SetFiness ::: 0=VeryCoarse, 1=Coarse, 2=Moderate, 3=Fine, 4=VeryFine, 5=Custom")
MeshFineness = float(raw_input("SetFineness[0~5] : "))
if MeshFineness==5:
	MeshSegPerEdge = float(raw_input("  MeshSegPerEdge[ea] : "))
	MeshSegPerRadius = float(raw_input("  MeshSegPerRadius[ea] : "))
	MeshGrowthRate = float(raw_input("  MeshGrowthRate[0~1] : "))


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
print("----------------------------------------------------")
print("----- Read STEP file ... ")
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
### SMESH component
#################################################
import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

# New Study
smesh = smeshBuilder.New(theStudy)

# New Mesh
MESH = smesh.Mesh(PARTITION)

# Parameters
NETGEN_2D3D = MESH.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_Parameters = NETGEN_2D3D.Parameters()
NETGEN_Parameters.SetMinSize( MinMeshSize )
NETGEN_Parameters.SetMaxSize( MaxMeshSize )
NETGEN_Parameters.SetSecondOrder( int(MeshSecondOrder) )
# SetFiness ::: 0=VeryCoarse, 1=Coarse, 2=Moderate, 3=Fine, 4=VeryFine, 5=Custom
if MeshFineness!=5:
	NETGEN_Parameters.SetFineness( int(MeshFineness) )
if MeshFineness==5:
	NETGEN_Parameters.SetGrowthRate( MeshGrowthRate )
	NETGEN_Parameters.SetNbSegPerEdge( MeshSegPerEdge )
	NETGEN_Parameters.SetNbSegPerRadius( MeshSegPerRadius )
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


#################################################
# Make MESH
#################################################
print("----------------------------------------------------")
print("----- Mesh Computing ... ")
isDone = MESH.Compute()


#################################################
# GROUP (INTERSECT FACES of PARTS)
#################################################
MGROUP_INTERSECTS = []
for fGROUP in range(0,len(MGROUP_FACES)):
	for fGROUP2 in range(fGROUP+1,len(MGROUP_FACES)):
		if fGROUP!=fGROUP2:
			aCriteria = []
			aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToMeshGroup,SMESH.FT_Undefined,MGROUP_FACES[fGROUP],SMESH.FT_Undefined,SMESH.FT_LogicalAND)
			aCriteria.append(aCriterion)
			aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToMeshGroup,SMESH.FT_Undefined,MGROUP_FACES[fGROUP2])
			aCriteria.append(aCriterion)
			aFilter = smesh.GetFilterFromCriteria(aCriteria)
			aFilter.SetMesh(MESH.GetMesh())
			info = []
			info = smesh.GetMeshInfo(aFilter)
			if info.values()[10]: # Dictionary Key : Entity_Quad_Triangle
				MGROUP_INTERSECTS.append( MESH.GroupOnFilter( SMESH.FACE, 'INTERSECT{0}'.format(fGROUP+1), aFilter ) )


#################################################
# GROUP (CUT FACES of PARTS)
#################################################
MGROUP_CUTS = []
for fGROUP in range(0,len(MGROUP_FACES)):
	aCriteria = []
	aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToMeshGroup,SMESH.FT_Undefined,MGROUP_FACES[fGROUP],SMESH.FT_Undefined,SMESH.FT_LogicalAND)
	aCriteria.append(aCriterion)
	for fGROUP2 in range(0,len(MGROUP_INTERSECTS)):
		aCriterion = smesh.GetCriterion(SMESH.FACE,SMESH.FT_BelongToMeshGroup,SMESH.FT_Undefined,MGROUP_INTERSECTS[fGROUP2],SMESH.FT_LogicalNOT)
		aCriteria.append(aCriterion)
	aFilter = smesh.GetFilterFromCriteria(aCriteria)
	aFilter.SetMesh(MESH.GetMesh())
	info = []
	info = smesh.GetMeshInfo(aFilter)
	if info!=smesh.GetMeshInfo(MGROUP_FACES[fGROUP]) and info.values()[10]:
		MGROUP_CUTS.append( MESH.GroupOnFilter( SMESH.FACE, 'CUT{0}'.format(fGROUP+1), aFilter ) )


#################################################
# Make UNV
#################################################
FILENAME_HEAD = os.path.splitext(FILENAME)[-2]
print("----------------------------------------------------")
print("----- Make UNV ... ")
try:
  MESH.ExportUNV( DIRECTORY+"/"+FILENAME_HEAD+".unv")
except:
  print 'ExportUNV() failed. Invalid file name?'


#################################################
# MESH Info
#################################################
print("----------------------------------------------------")
print "Information about mesh:" 
print "Number of nodes       : ", MESH.NbNodes()
print "Number of edges       : ", MESH.NbEdges()
print "Number of faces       : ", MESH.NbFaces()
print "          triangles   : ", MESH.NbTriangles()
print "          quadrangles : ", MESH.NbQuadrangles()
print "          polygons    : ", MESH.NbPolygons()
print "Number of volumes     : ", MESH.NbVolumes()
print "          tetrahedrons: ", MESH.NbTetras()
print "          hexahedrons : ", MESH.NbHexas()
print "          prisms      : ", MESH.NbPrisms()
print "          pyramids    : ", MESH.NbPyramids()
print "          polyhedrons : ", MESH.NbPolyhedrons() 
print("----------------------------------------------------")
print("----- FINISHED ! -----")


#################################################
# DISPLAY
#################################################
#if salome.sg.hasDesktop():
#  salome.sg.updateObjBrowser(True)


