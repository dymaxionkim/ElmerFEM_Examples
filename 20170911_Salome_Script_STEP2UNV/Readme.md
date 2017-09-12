
# STEP2UNV for Elmer with Salome (V02)

_Import, Grouping and Meshing for a STEP File_


## PreRequisite
* Linux OS
* ElmerGUI
* Salome Platform 8.2


## Install

* Download and Path

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

* Check Salome excecutor's path. If necessary, modify `step2unv` file.


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
#################################################
aaa.unv
#################################################
Finished!
```

* Open `.unv` in ElmerGUI.
* Check Body groups.
* Check Surface groups.
