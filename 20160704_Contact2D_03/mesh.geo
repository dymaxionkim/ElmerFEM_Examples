// Gmsh project created on Wed Jun 22 20:56:03 2016

// 실험결과 요약
// 1. 2개의 Body를 모두 gmsh에서 만들어 Elmer로 넘기면 해석에 100% 실패한다.
// 2. 따로따로 gmsh에서 싱글바디를 만들어 ElmerGrid로 합치면, 각 엔티티들의 넘버링이 겹쳐서 중복되어 버리므로 실패.
// 3. 하나의 gmsh  파일에서 2개의 바디를 만들어 넘기면, 넘버링 겹치는 현상은 피할 수 있으나, 해석에서는 깨져 버린다.
// 4. 하나는 gmsh로, 또 하나는 ElmerGRid로 생성해서 합치면 이상없이 해석이 된다.
// 5. 이유는 정확히 모르겠다...  아무튼 gmsh만으로 멀티바디 해석은 현 시점에서 어렵다.

// Tire
R = 0.25;  // Radius
Ra = 0.1;  // Axis Radius
Gap = 0.0;  // Initial Gap
Resolution = 20;

Point(1) = {0, Gap+R, 0, 1.0};

Point(2) = {0, Gap+R+R, 0, 1.0};
Point(3) = {R, Gap+R, 0, 1.0};
Point(4) = {0, Gap+0, 0, 1.0};
Point(5) = {-R, Gap+R, 0, 1.0};

Circle(1) = {2,1,3};
Circle(2) = {3,1,4};
Circle(3) = {4,1,5};
Circle(4) = {5,1,2};

Point(6) = {0, Gap+R+Ra, 0, 1.0};
Point(7) = {Ra, Gap+R, 0, 1.0};
Point(8) = {0, Gap+R-Ra, 0, 1.0};
Point(9) = {-Ra, Gap+R, 0, 1.0};

Circle(5) = {6,1,7};
Circle(6) = {7,1,8};
Circle(7) = {8,1,9};
Circle(8) = {9,1,6};

Line Loop(11) = {1,2,3,4};
Line Loop(12) = {5,6,7,8};
Plane Surface(13) = {11,-12};

Transfinite Line {1,5} = Resolution Using Progression 1;
Transfinite Line {2,6} = Resolution Using Progression 1;
Transfinite Line {3,7} = Resolution Using Progression 1;
Transfinite Line {4,8} = Resolution Using Progression 1;






// Ground
W = 0.5; // Ground width

Point(101) = {-W, 0, 0, 1.0};
Point(102) = {W, 0, 0, 1.0};
Point(103) = {W, -0.1, 0, 1.0};
Point(104) = {-W, -0.1, 0, 1.0};

Line(101) = {101, 102};
Line(102) = {102, 103};
Line(103) = {103, 104};
Line(104) = {104, 101};

Line Loop(101) = {101, 102, 103, 104};
Plane Surface(101) = {101};

Transfinite Line {101, 103} = 50 Using Progression 1;
Transfinite Line {104, 102} = 10 Using Progression 1;

Transfinite Surface {101};
Recombine Surface {101};

