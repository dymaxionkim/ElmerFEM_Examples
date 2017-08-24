#!/bin/bash
###########################################################
# Custom Materials
# 2017.08.24
# by Dymaxion.kim@gmail.com
###########################################################

sudo mv /usr/share/ElmerGUI/edf/egmaterials.xml /usr/share/ElmerGUI/edf/egmaterials.xml.old

sudo ln -s ~/github/ElmerFEM_Examples/egmaterials.xml /usr/share/ElmerGUI/edf/egmaterials.xml

exit 0

