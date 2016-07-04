#!/bin/bash

gmsh mesh.geo -2 -order 2 -o mesh.msh

ElmerGrid 14 2 mesh.msh -autoclean

ElmerSolver ./mesh.sif

rm ./p1.dat
rm ./p1_rsum.dat
rm ./TEST.PASSED
