// Modeling of CONTACT
// 20210426 Dymaxion.Kim@gmail.com

// Command
// /home/osboxes/.Gmsh/bin/gmsh ./CONTACT2.geo

// Input Parameters
DO = 100.000e-3; // Outer Diameter of Ring
lc =  DO/100; // Mesh Size

// Ring
Point(1) = {0,     0+DO/2,     0,lc}; // Actual Center

Point(2) = {DO/2,  0+DO/2,     0,lc};
Point(3) = {0,     DO/2+DO/2,  0,lc};
Point(4) = {-DO/2, 0+DO/2,     0,lc};
Point(5) = {0,     -DO/2+DO/2, 0,lc};

Circle(1) = {2,1,3};
Circle(2) = {3,1,4};
Circle(3) = {4,1,5};
Circle(4) = {5,1,2};

Line Loop(1) = {1,2,3,4};
Plane Surface(1) = {1};

// BOT
Point(21) = {-DO,     0,  0,lc};
Point(22) = { DO,     0,  0,lc};
Point(23) = { DO, -DO/4,  0,lc};
Point(24) = {-DO, -DO/4,  0,lc};

Line(21) = {21,22};
Line(22) = {22,23};
Line(23) = {23,24};
Line(24) = {24,21};

Line Loop(21) = {21,22,23,24};
Plane Surface(21) = {21};

// TOP
Point(31) = {-DO,      DO,  0,lc};
Point(32) = { DO,      DO,  0,lc};
Point(33) = { DO, DO+DO/4,  0,lc};
Point(34) = {-DO, DO+DO/4,  0,lc};

Line(31) = {31,32};
Line(32) = {32,33};
Line(33) = {33,34};
Line(34) = {34,31};

Line Loop(31) = {31,32,33,34};
Plane Surface(31) = {31};


// Mesh
Mesh 2;
Save "CONTACT2.unv";
