
# Modified salome multibody CAD import for elmer

_Import, Grouping and Meshing for Multi STEP Files_


## PreRequisite
* Linux OS
* ElmerGUI
* Salome Platform


## Install

* Download and Path

```bash
mkdir ~/.config/salome/cad_import
wget -O ~/.config/salome/cad_import/cad_import.sh https://raw.githubusercontent.com/dymaxionkim/ElmerFEM_Examples/master/20170902_Salome_Script_cad_import/cad_import.sh
wget -O ~/.config/salome/cad_import/cad_import.py https://raw.githubusercontent.com/dymaxionkim/ElmerFEM_Examples/master/20170902_Salome_Script_cad_import/cad_import.py
wget -O ~/.config/salome/cad_import/Readme.md https://raw.githubusercontent.com/dymaxionkim/ElmerFEM_Examples/master/20170902_Salome_Script_cad_import/Readme.md
chmod +x ~/.config/salome/cad_import/cad_import.sh
echo "" >> ~/.bashrc
echo "# Modified salome multibody CAD import for elmer" >> ~/.bashrc
echo "export PATH=\"/home/MYHOME/.config/salome/cad_import:\$PATH\"" >> ~/.bashrc
echo "" >> ~/.bashrc
```

* Check Salome excecutor's path. If necessary, modify `cad_import.sh` file.


## How to use

* Prepare geometry files
  - Format : STEP
  - File Extension : .step (not .stp)
  - One part per one STEP file (No assembly strucures in one STEP file)
  - Every STEP files should be one working directory.
  - STEP files should be over two. (Not single file)

* Excecute script

```bash
cad_import.sh
```

* Interact

```bash
Input your working directory path : /home/MYHOME/work
...
MinMeshSize[mm] : 1
MaxMeshSize[mm] : 5
MeshSegPerEdge[ea] : 50
MeshGrowthRate[0~1] : 0.7
```

* Wait and Check

```bash
#################################################
Mesh.unv
#################################################
Finished!
```

* Open `Mesh.unv` in ElmerGUI.
* Check Body groups.
* Devide Surface groups in ElmerGUI.





