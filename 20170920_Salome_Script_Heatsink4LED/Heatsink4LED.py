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
QTY_X = 3
QTY_Y = 2
PITCH_X = 0.01
PITCH_Y = 0.02
MARGIN_X = 0.01
MARGIN_Y = 0.015
PCB_X = (QTY_X-1)*PITCH_X+2*MARGIN_X
PCB_Y = (QTY_Y-1)*PITCH_Y+2*MARGIN_Y
PCB_Z = 0.0012
TIM_X = PCB_X
TIM_Y = PCB_Y
TIM_Z = 0.0005
MARGIN_BASE_X = 0.01
MARGIN_BASE_Y = 0.01
BASE_X = PCB_X+2*MARGIN_BASE_X
BASE_Y = PCB_Y+2*MARGIN_BASE_Y
BASE_Z = 0.005
QTY_FIN = 20
FIN_X = 0.002
FIN_Y = BASE_Y
FIN_Z = 0.015

#################################################
## New Study
#################################################
geompy = geomBuilder.New(theStudy)

"""
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
"""

#################################################
## SLUG and Solid LED Cores
#################################################
SLUG = []
LED = []
for qty_x in range(0,QTY_X):
	for qty_y in range(0,QTY_Y):
		SLUG.append( geompy.MakeBoxDXDYDZ(SLUG_X, SLUG_Y, SLUG_Z) )
		geompy.TranslateDXDYDZ(SLUG[-1], -SLUG_X/2+qty_x*PITCH_X, -SLUG_Y/2+qty_y*PITCH_Y, 0)
		geompy.addToStudy( SLUG[-1], 'SLUG' )
		LED.append( geompy.MakeBoxDXDYDZ(LED_X, LED_Y, LED_Z) )
		geompy.TranslateDXDYDZ(LED[-1], -LED_X/2+qty_x*PITCH_X, -LED_Y/2+qty_y*PITCH_Y, SLUG_Z)
		geompy.addToStudy( LED[-1], 'LED' )

#################################################
## PCB
#################################################
PCB = geompy.MakeBoxDXDYDZ( PCB_X, PCB_Y, PCB_Z )
geompy.TranslateDXDYDZ( PCB, -MARGIN_X, -MARGIN_Y, -PCB_Z )
geompy.addToStudy( PCB, 'PCB' )

#################################################
## TIM
#################################################
TIM = geompy.MakeBoxDXDYDZ( TIM_X, TIM_Y, TIM_Z )
geompy.TranslateDXDYDZ( TIM, -MARGIN_X, -MARGIN_Y, -(PCB_Z+TIM_Z) )
geompy.addToStudy( TIM, 'TIM' )

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
geompy.addToStudy( HEATSINK, 'HEATSINK' )

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
## View Study
#################################################
if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
