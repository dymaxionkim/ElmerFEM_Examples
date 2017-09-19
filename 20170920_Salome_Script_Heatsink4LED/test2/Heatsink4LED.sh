#!/bin/bash
###########################################################
# Heatsink4LED for Elmer with Salome
# Auto Modeling, Import, Grouping and Meshing
# Export mesh.hdf & mesh.unv
# 2017.09.20
# by Dymaxion.kim@gmail.com
###########################################################

StartTime=$(date +%s)

salome -t ./Heatsink4LED.py
salome killall
ElmerGrid 8 2 mesh.unv -autoclean
rm -R case
mkdir case
ElmerSolver case.sif

EndTime=$(date +%s)
echo "It takes $(($EndTime - $StartTime)) seconds to complete this task."

exit 0


