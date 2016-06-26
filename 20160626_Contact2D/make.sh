#! /bin/bash

gmsh -2 -optimize_netgen blunt.geo -o blunt.msh
ElmerGrid 14 2 blunt.msh -autoclean
ElmerGrid 1 2 base.grd
ElmerGrid 2 2 blunt -in base -unite -out mesh

ElmerSolver

