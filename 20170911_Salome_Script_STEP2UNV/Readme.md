
# STEP2UNV for Elmer with Salome (V02)

_Import, Grouping and Meshing for a STEP File_


## PreRequisite
* Linux OS / Windows OS
* ElmerGUI
* Salome Platform 8.2


## Install

* Download and Path (on Linux)

```bash
mkdir ~/.config/salome/step2unv
wget -O ~/.config/salome/step2unv/step2unv https://raw.githubusercontent.com/dymaxionkim/ElmerFEM_Examples/master/20170911_Salome_Script_STEP2UNV/step2unv
wget -O ~/.config/salome/step2unv/step2unv.py https://raw.githubusercontent.com/dymaxionkim/ElmerFEM_Examples/master/20170911_Salome_Script_STEP2UNV/step2unv.py
wget -O ~/.config/salome/step2unv/Readme.md https://raw.githubusercontent.com/dymaxionkim/ElmerFEM_Examples/master/20170911_Salome_Script_STEP2UNV/Readme.md
chmod +x ~/.config/salome/step2unv/step2unv
echo "" >> ~/.bashrc
echo "# STEP2UNV for Elmer with Salome" >> ~/.bashrc
echo "export PATH=\"/home/MYHOME/.config/salome/step2unv:\$PATH\"" >> ~/.bashrc
echo "" >> ~/.bashrc
```

* Download and Path (on Windows)

Install Salome platform Windows version in `C:\Salome`.

Download next files in `C:\Salome\STEP2UNV` :

```bash
https://github.com/dymaxionkim/ElmerFEM_Examples/raw/master/20170911_Salome_Script_STEP2UNV/step2unv.py
https://github.com/dymaxionkim/ElmerFEM_Examples/raw/master/20170911_Salome_Script_STEP2UNV/step2unv.bat
```

Add path in `path` system variable like this :

```bash
C:\Salome\SALOME-8.2.0-WIN64\WORK
C:\Salome\STEP2UNV
```

* Check Salome excecutor's path. If necessary, modify `step2unv` file. (on Linux)


## How to use

* Prepare geometry files
  - Format : STEP
  - Single STEP file that includes multi bodies
  - No interferences with two bodies, but only Contact
  - The STEP files should be in the working directory

* Excecute script

```bash
$ step2unv
```

* Interactive Input

```bash
...
Input your working directory path : /home/MYHOME/work
Input your STEP File Name : aaa.step
Hypothesys for NETGEN
MinMeshSize[mm] : 10
MaxMeshSize[mm] : 200
MeshSegPerEdge[ea] : 50
MeshSegPerRadius[ea] : 20
MeshGrowthRate[0~1] : 0.6
...
```

* Wait and Check

```bash
Information about mesh:
Number of nodes       : ...
Number of edges       : ...
Number of faces       : ...
          triangles   : ...
          quadrangles : ...
          polygons    : ...
Number of volumes     : ...
          tetrahedrons: ...
          hexahedrons : ...
          prisms      : ...
          pyramids    : ...
          polyhedrons : ...
```

* Open `.unv` in ElmerGUI.
* Check Body groups.
* Check Surface groups.


## Example

* 3D Multibodies Modeling with FreeCAD

![20170912_001](https://user-images.githubusercontent.com/12775748/30309522-bfa2e43a-97c6-11e7-8cab-a8246999e3a2.png)

* Run in terminal

![20170912_002](https://user-images.githubusercontent.com/12775748/30309526-c3019e14-97c6-11e7-9536-bce2786d3b4f.png)

* Input working directory and STEP file name

![20170912_003](https://user-images.githubusercontent.com/12775748/30309528-c4fd4c68-97c6-11e7-8dc1-54e10368b571.png)

* Input Netgen parameters

![20170912_004](https://user-images.githubusercontent.com/12775748/30309530-c64e9be4-97c6-11e7-94f6-824e3d80033e.png)

* Open UNV file in ElmerGUI

![20170912_005](https://user-images.githubusercontent.com/12775748/30309534-c830b6c2-97c6-11e7-9e46-ddd6087e9d9e.png)

* Check surface groups

![20170912_006](https://user-images.githubusercontent.com/12775748/30309536-c98bb6ca-97c6-11e7-9c47-8c9b97fa0452.png)


## Thank you!
