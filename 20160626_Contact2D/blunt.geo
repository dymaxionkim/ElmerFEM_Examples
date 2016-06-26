cl__1 = 1e+22;
Radius = 1;
RadiusAxis = 0.5;
Resolution = 100;

Point(1) = {0, Radius, 0, cl__1};

Point(2) = {0, 0, 0, cl__1};
Point(3) = {-Radius, Radius, 0, cl__1};
Point(4) = {0, Radius+Radius, 0, cl__1};
Point(5) = {Radius, Radius, 0, cl__1};

Point(6) = {0, Radius-RadiusAxis, 0, cl__1};
Point(7) = {-RadiusAxis, Radius, 0, cl__1};
Point(8) = {0, Radius+RadiusAxis, 0, cl__1};
Point(9) = {RadiusAxis, Radius, 0, cl__1};

Circle(1) = {5, 1, 2};
Circle(2) = {2, 1, 3};
Circle(3) = {3, 1, 4};
Circle(4) = {4, 1, 5};

Circle(5) = {9, 1, 6};
Circle(6) = {6, 1, 7};
Circle(7) = {7, 1, 8};
Circle(8) = {8, 1, 9};

Line Loop(5) = {1, 2, 3, 4};
Line Loop(6) = {5, 6, 7, 8};

Plane Surface(7) = {5, 6};

Transfinite Line {3, 7} = Resolution Using Progression 1;
Transfinite Line {4, 8} = Resolution Using Progression 1;
Transfinite Line {1, 5} = Resolution Using Progression 1;
Transfinite Line {2, 6} = Resolution Using Progression 1;
//Transfinite Surface {7};
Recombine Surface {7};

//Mesh.ElementOrder = 2;



