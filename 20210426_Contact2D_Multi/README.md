# Mechanical Contact 2D

_Multi Faces_



## 1. Pre-requisites

* gmsh
* ElmerFEM
* Paraview



## 2. Commands

```bash
code CONTACT2.geo
gmsh CONTACT2.geo
ElmerGrid 8 2 CONTACT2.unv
cd CONTACT2
ElmerSolver
paraview
```



## 3. Result

[![CONTACT2](https://user-images.githubusercontent.com/12775748/116086351-b1bd8100-a6da-11eb-83bf-d7c6a0fb480d.png)](https://youtu.be/a2JDrV54QPM)



