cl__1 = 1;
cl__2 = 0.5;
Point(1) = {0, 0, 0, 1};
Point(2) = {500, 0, 0, 1};
Point(3) = {500, 200, 0, 1};
Point(4) = {0, 200, 0, 1};
Point(5) = {200, 100, 0, 1};
Point(6) = {180, 100, 0, 0.5};
Point(8) = {200, 120, 0, 0.5};
Point(9) = {200, 80, 0, 0.5};
Point(10) = {220, 100, 0, 0.5};
Line(1) = {4, 1};
Transfinite Line {1} = 30 Using Progression 1;
Line(2) = {3, 2};
Transfinite Line {2} = 30 Using Progression 1;
Line(3) = {4, 3};
Transfinite Line {3} = 50 Using Progression 1;
Line(4) = {1, 2};
Transfinite Line {4} = 50 Using Progression 1;
Circle(6) = {6, 5, 10};
Circle(7) = {10, 5, 6};
Line Loop(10) = {3, 2, -4, -1, -6, -7};
Plane Surface(10) = {10};
Recombine Surface {10};