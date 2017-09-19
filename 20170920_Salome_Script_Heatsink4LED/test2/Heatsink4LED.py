# -*- coding: utf-8 -*-

#################################################
#
#   Heatsink4LED for Elmer with Salome
#   V01
#
#   Data: 2017-09-18
#   Modifier : DymaxionKim
#
#   - Salome 8.2
#   - Assy of SMT LED Packages Array, PCB Layer, TIM Layer, and Heatsink with linear fins
#   - Auto Grouping
#   - Auto Meshing
#
#################################################

import sys
import salome
import os

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/osboxes/WORK')

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


#################################################
## Geometrical Parameters
#################################################
SLUG_X = 0.005
SLUG_Y = 0.005
SLUG_Z = 0.0004
LED_X = 0.0005
LED_Y = 0.0015
LED_Z = 0.000015
QTY_X = 6
QTY_Y = 20
PITCH_X = 0.014
PITCH_Y = 0.0128
MARGIN_X = 0.0075
MARGIN_Y = 0.0075
PCB_X = (QTY_X-1)*PITCH_X+2*MARGIN_X
PCB_Y = (QTY_Y-1)*PITCH_Y+2*MARGIN_Y
PCB_Z = 0.001
TIM_X = PCB_X
TIM_Y = PCB_Y
TIM_Z = 0.00005
MARGIN_BASE_X = 0.009
MARGIN_BASE_Y = 0.02
BASE_X = PCB_X+2*MARGIN_BASE_X
BASE_Y = PCB_Y+2*MARGIN_BASE_Y
BASE_Z = 0.004
QTY_FIN = 8
FIN_X = 0.006
FIN_Y = BASE_Y
FIN_Z = 0.008


#################################################
## Mesh Parameters
#################################################
MinMeshSize = 0.0000001 # specify in m
MaxMeshSize = 0.003 # specify in m
#MeshSecondOrder = float(raw_input("SetSecondOrder[0,1] : "))
MeshSecondOrder = 1
#SetFiness ::: 0=VeryCoarse, 1=Coarse, 2=Moderate, 3=Fine, 4=VeryFine, 5=Custom"
MeshFineness = 5
if MeshFineness==5:
	MeshSegPerEdge = 5
	MeshSegPerRadius = 5
	MeshGrowthRate = 0.1


#################################################
## Input Parameters in TUI
#################################################
print("----------------------------------------------------")
SLUG_X = 0.005
SLUG_Y = 0.005
SLUG_Z = 0.0004
LED_X = 0.0005
LED_Y = 0.0015
LED_Z = 0.000015
print("Qty of LED by X-direction [ea] :")
QTY_X = int(raw_input())
print("Qty of LED by Y-direction [ea] :")
QTY_Y = int(raw_input())
print("Pitch of LED by X-direction [m] :")
PITCH_X = float(raw_input())
print("Pitch of LED by Y-direction [m] :")
PITCH_Y = float(raw_input())
print("Distance from PCB's edge to LED by X-direction [m] :")
MARGIN_X = float(raw_input())
print("Distance from PCB's edge to LED by Y-direction [m] :")
MARGIN_Y = float(raw_input())
PCB_X = (QTY_X-1)*PITCH_X+2*MARGIN_X
PCB_Y = (QTY_Y-1)*PITCH_Y+2*MARGIN_Y
PCB_Z = 0.001
TIM_X = PCB_X
TIM_Y = PCB_Y
TIM_Z = 0.00005
print("Distance from HEATSINK's edge to PCB's edge X-direction [m] :")
MARGIN_BASE_X = float(raw_input())
print("Distance from HEATSINK's edge to PCB's edge Y-direction [m] :")
MARGIN_BASE_Y = float(raw_input())
BASE_X = PCB_X+2*MARGIN_BASE_X
BASE_Y = PCB_Y+2*MARGIN_BASE_Y
print("Thickness of HEATSINK's base [m] :")
BASE_Z = float(raw_input())
print("Qty of HEATSINK's fins [ea] :")
QTY_FIN = int(raw_input())
print("RATIO_FIN [(Fin's Width)/(Distance by two fins)] :")
RATIO_FIN = float(raw_input())
FIN_X = RATIO_FIN*(2*(MARGIN_X+MARGIN_BASE_X)+(QTY_X-1.0)*PITCH_X) / ((QTY_FIN-1)*(1-RATIO_FIN)+QTY_FIN*RATIO_FIN)
FIN_Y = BASE_Y
print("Height of HEATSINK's fins [m] :")
FIN_Z = float(raw_input())


#################################################
## New Study
#################################################
print("----------------------------------------------------")
print("----- New Geometrical Study ... ")
geompy = geomBuilder.New(theStudy)


#################################################
## SLUG and Solid LED Cores
#################################################
SLUG = []
LED = []
for qty_x in range(0,QTY_X):
	for qty_y in range(0,QTY_Y):
		SLUG.append( geompy.MakeBoxDXDYDZ(SLUG_X, SLUG_Y, SLUG_Z) )
		geompy.TranslateDXDYDZ(SLUG[-1], -SLUG_X/2+qty_x*PITCH_X, -SLUG_Y/2+qty_y*PITCH_Y, 0)
		#geompy.addToStudy( SLUG[-1], 'SLUG' )
		LED.append( geompy.MakeBoxDXDYDZ(LED_X, LED_Y, LED_Z) )
		geompy.TranslateDXDYDZ(LED[-1], -LED_X/2+qty_x*PITCH_X, -LED_Y/2+qty_y*PITCH_Y, SLUG_Z)
		#geompy.addToStudy( LED[-1], 'LED' )


#################################################
## PCB
#################################################
PCB = geompy.MakeBoxDXDYDZ( PCB_X, PCB_Y, PCB_Z )
geompy.TranslateDXDYDZ( PCB, -MARGIN_X, -MARGIN_Y, -PCB_Z )
#geompy.addToStudy( PCB, 'PCB' )


#################################################
## TIM
#################################################
TIM = geompy.MakeBoxDXDYDZ( TIM_X, TIM_Y, TIM_Z )
geompy.TranslateDXDYDZ( TIM, -MARGIN_X, -MARGIN_Y, -(PCB_Z+TIM_Z) )
#geompy.addToStudy( TIM, 'TIM' )


#################################################
## HEATSINK
#################################################
BASE = geompy.MakeBoxDXDYDZ( BASE_X, BASE_Y, BASE_Z )
geompy.TranslateDXDYDZ( BASE, -(MARGIN_X+MARGIN_BASE_X), -(MARGIN_Y+MARGIN_BASE_Y), -(PCB_Z+TIM_Z+BASE_Z) )
#geompy.addToStudy( BASE, 'BASE' )

FIN = []
for qty_fin in range(0,QTY_FIN):
	FIN.append( geompy.MakeBoxDXDYDZ(FIN_X, FIN_Y, FIN_Z) )
	geompy.TranslateDXDYDZ( FIN[-1], qty_fin*(BASE_X-FIN_X)/(QTY_FIN-1)-(MARGIN_X+MARGIN_BASE_X), -(MARGIN_Y+MARGIN_BASE_Y), -(PCB_Z+TIM_Z+BASE_Z+FIN_Z) )
	#geompy.addToStudy( FIN[-1], 'FIN' )

FINS_INDEX = []
FINS_INDEX.append(BASE)
for qty_fin in range(0,QTY_FIN):
	FINS_INDEX.append(FIN[qty_fin])
HEATSINK = geompy.MakeFuseList( FINS_INDEX, True, True )
#geompy.addToStudy( HEATSINK, 'HEATSINK' )


#################################################
## PARTITION
#################################################
PARTS = []
PARTS.append(HEATSINK)
PARTS.append(TIM)
PARTS.append(PCB)
for slug in range(0,len(SLUG)):
	PARTS.append(SLUG[slug])
for led in range(0,len(LED)):
	PARTS.append(LED[led])

PARTITION = geompy.MakePartition(PARTS, [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
PARTS = geompy.ExtractShapes(PARTITION, geompy.ShapeType["SOLID"], False)


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

UNION_SLUG = []
ID_UNION_SLUG = []
for aGROUP in range(3,QTY_X*QTY_Y+3):
	ID_UNION_SLUG.append( GROUP_PARTS[aGROUP] )
UNION_SLUG = geompy.UnionListOfGroups(ID_UNION_SLUG)

UNION_LED = []
ID_UNION_LED = []
for aGROUP in range(QTY_X*QTY_Y+3,len(PARTS)):
	ID_UNION_LED.append( GROUP_PARTS[aGROUP] )
UNION_LED = geompy.UnionListOfGroups(ID_UNION_LED)

# Add to Study
geompy.addToStudy( PARTITION, 'PARTITION' )
geompy.addToStudyInFather( PARTITION, GROUP_PARTS[0], 'HEATSINK' )
geompy.addToStudyInFather( PARTITION, GROUP_PARTS[1], 'TIM' )
geompy.addToStudyInFather( PARTITION, GROUP_PARTS[2], 'PCB' )
geompy.addToStudyInFather( PARTITION, UNION_SLUG, 'SLUG' )
geompy.addToStudyInFather( PARTITION, UNION_LED, 'LED' )

#for aGROUP in range(3,QTY_X*QTY_Y+3):
#	geompy.addToStudyInFather( PARTITION, GROUP_PARTS[aGROUP], 'SLUG{0}'.format(aGROUP+1-3) )
#for aGROUP in range(QTY_X*QTY_Y+3,len(PARTS)):
#	geompy.addToStudyInFather( PARTITION, GROUP_PARTS[aGROUP], 'LED{0}'.format(aGROUP+1-9) )


#################################################
### SMESH component
#################################################
print("----------------------------------------------------")
print("----- New SMESH Study ... ")
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
MGROUP_PARTS.append( MESH.GroupOnGeom(GROUP_PARTS[0], 'HEATSINK', SMESH.VOLUME) )
MGROUP_PARTS.append( MESH.GroupOnGeom(GROUP_PARTS[1], 'TIM', SMESH.VOLUME) )
MGROUP_PARTS.append( MESH.GroupOnGeom(GROUP_PARTS[2], 'PCB', SMESH.VOLUME) )
MGROUP_PARTS.append( MESH.GroupOnGeom(UNION_SLUG, 'SLUG', SMESH.VOLUME) )
MGROUP_PARTS.append( MESH.GroupOnGeom(UNION_LED, 'LED', SMESH.VOLUME) )


#################################################
# GROUP (FACES of PARTS)
#################################################
MGROUP_FACES = []
MGROUP_FACES.append( MESH.GroupOnGeom(GROUP_PARTS[0], 'HEATSINK', SMESH.FACE) )
MGROUP_FACES.append( MESH.GroupOnGeom(GROUP_PARTS[1], 'TIM', SMESH.FACE) )
MGROUP_FACES.append( MESH.GroupOnGeom(GROUP_PARTS[2], 'PCB', SMESH.FACE) )
MGROUP_FACES.append( MESH.GroupOnGeom(UNION_SLUG, 'SLUG', SMESH.FACE) )
MGROUP_FACES.append( MESH.GroupOnGeom(UNION_LED, 'LED', SMESH.FACE) )


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
print("----------------------------------------------------")
print("----- Make UNV ... ")
DIRECTORY = os.getcwd()
try:
  MESH.ExportUNV( DIRECTORY+"/"+"mesh.unv")
except:
  print 'ExportUNV() failed. Invalid file name?'


#################################################
# Save HDF
#################################################
print("----------------------------------------------------")
print("----- Save HDF ... ")
salome.myStudyManager.SaveAs(DIRECTORY+"/"+"Study.hdf",salome.myStudy,False)


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
## View Study
#################################################
#if salome.sg.hasDesktop():
#  salome.sg.updateObjBrowser(True)

