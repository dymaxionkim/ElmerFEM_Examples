
# Modified salome multibody CAD import for elmer

_Import, Grouping and Meshing for Multi STEP Files_
_Original coding by Rainer Ochs_
_Modified by DymaxionKim_



## PreRequisite
* Linux OS (maybe possible in Windows OS)
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

![](https://user-images.githubusercontent.com/12775748/29995790-900ebe34-902c-11e7-9ae6-2db575a25a66.png)


* Excecute script

```bash
cad_import.sh
```

![](https://user-images.githubusercontent.com/12775748/29995791-900f0006-902c-11e7-9c98-ad288aa25f80.png)


* Interact

```bash
Input your working directory path : /home/MYHOME/work
...
MinMeshSize[mm] : 1
MaxMeshSize[mm] : 5
MeshSegPerEdge[ea] : 50
MeshGrowthRate[0~1] : 0.7
```

![](https://user-images.githubusercontent.com/12775748/29995795-903d8ae8-902c-11e7-9cef-c15b48b50c46.png)

![](https://user-images.githubusercontent.com/12775748/29995796-9043ec44-902c-11e7-9b77-548bad9112b0.png)


* Wait and Check

```bash
...
#################################################
Mesh.unv
#################################################
Finished!
```

![](https://user-images.githubusercontent.com/12775748/29995794-90390324-902c-11e7-993c-1bc1faab5b4c.png)

![](https://user-images.githubusercontent.com/12775748/29995793-90337738-902c-11e7-958d-216316609b51.png)


* Open `Mesh.unv` in ElmerGUI.

![](https://user-images.githubusercontent.com/12775748/29995792-90337c74-902c-11e7-9c1d-2185980e47a6.png)

![](https://user-images.githubusercontent.com/12775748/29995798-9057f040-902c-11e7-9299-2e7dbe7cc348.png)


* Check Body groups. (Body 1, Body 2, ...)
* Devide Surface groups in ElmerGUI. (in ElmerGUI Menu, `Mesh - Divide surface..`)


_Thank you!_
