cl = 1;
Depth_Dermis = 0.0015;
Depth_Fat = 0.003;
Depth_Muscle = 0.005;
Width = 0.02;
Segment = 20000;

Point(1) = {0, 0, 0, cl};
Point(2) = {-Width/2, 0, 0, cl};
Point(3) = {-Width/2, -Depth_Dermis, 0, cl};
Point(4) = {-Width/2, -(Depth_Dermis+Depth_Fat), 0, cl};
Point(5) = {-Width/2, -(Depth_Dermis+Depth_Fat+Depth_Muscle), 0, cl};
Point(6) = {Width/2, -(Depth_Dermis+Depth_Fat+Depth_Muscle), 0, cl};
Point(7) = {Width/2, -(Depth_Dermis+Depth_Fat), 0, cl};
Point(8) = {Width/2, -Depth_Dermis, 0, cl};
Point(9) = {Width/2, 0, 0, cl};

Line(1) = {8, 9};
Transfinite Line {1} = Depth_Dermis*Segment Using Progression 1;
Line(2) = {9, 2};
Transfinite Line {2} = Width*Segment Using Progression 1;
Line(3) = {2, 3};
Transfinite Line {3} = Depth_Dermis*Segment Using Progression 1;
Line(4) = {3, 4};
Transfinite Line {4} = Depth_Fat*Segment Using Progression 1;
Line(5) = {4, 5};
Transfinite Line {5} = Depth_Muscle*Segment Using Progression 1;
Line(6) = {5, 6};
Transfinite Line {6} = Width*Segment Using Progression 1;
Line(7) = {6, 7};
Transfinite Line {7} = Depth_Muscle*Segment Using Progression 1;
Line(8) = {7, 8};
Transfinite Line {8} = Depth_Fat*Segment Using Progression 1;
Line(9) = {8, 3};
Transfinite Line {9} = Width*Segment Using Progression 1;
Line(10) = {7, 4};
Transfinite Line {10} = Width*Segment Using Progression 1;

Line Loop(1) = {2, 3, -9, 1};
Plane Surface(1) = {1};
Transfinite Surface {1};
Recombine Surface {1};

Line Loop(2) = {9, 4, -10, 8};
Plane Surface(2) = {2};
Transfinite Surface {2};
Recombine Surface {2};

Line Loop(3) = {10, 5, 6, 7};
Plane Surface(3) = {3};
Transfinite Surface {3};
Recombine Surface {3};

Physical Line("Dermis_Top") = {2};
Physical Line("Dermis-Fat") = {9};
Physical Line("Fat-Muscle") = {10};
Physical Line("Dermis_Side") = {1, 3};
Physical Line("Fat_Side") = {4, 8};
Physical Line("Muscle_Side") = {5, 7};
Physical Line("Muscle_Bot") = {6};
Physical Surface("Dermis") = {1};
Physical Surface("Fat") = {2};
Physical Surface("Muscle") = {3};

