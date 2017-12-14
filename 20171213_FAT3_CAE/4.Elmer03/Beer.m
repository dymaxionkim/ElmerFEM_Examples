
Depth_Dermis = 0.0015;
Depth_Fat = 0.005;
Depth_Muscle = 0.020;
Width = 0.06;
Segment = 5000;

r_Dermis = -Width/2:1/Segment:Width/2;
r_Fat = r_Dermis;
r_Muscle = r_Dermis;

z_Dermis = -Depth_Dermis:1/Segment:0.0;
z_Fat = -(Depth_Dermis+Depth_Fat):1/Segment:-Depth_Dermis;
z_Muscle = -(Depth_Dermis+Depth_Fat+Depth_Muscle):1/Segment:-(Depth_Dermis+Depth_Fat);

[R_Dermis,Z_Dermis] = meshgrid(r_Dermis,z_Dermis);
[R_Fat,Z_Fat] = meshgrid(r_Fat,z_Fat);
[R_Muscle,Z_Muscle] = meshgrid(r_Muscle,z_Muscle);

I0 = 2000.0; #[W/m^2], the irradiation intensity at the skin surface
sigma = 0.002; #[m], the width of the irradiated region (the standard deviation of the Gaussian function which describes the beam profile)
Absorptivity_Dermis = 0.0012; #[1/m]
Absorptivity_Fat = 0.0009; #[1/m]
Absorptivity_Muscle = 0.003; #[1/m]

Q_Dermis = I0*Absorptivity_Dermis*exp(Absorptivity_Dermis*Z_Dermis-R_Dermis.^2)./(2*sigma^2);
Q_Fat = Absorptivity_Fat*exp(Absorptivity_Fat*Z_Fat-R_Fat.^2)./(2*sigma^2);
Q_Fat = ones(size(Q_Fat)(1),size(Q_Fat)(2)).*Q_Dermis(1,:) .* Q_Fat
Q_Muscle = I0*Absorptivity_Muscle*exp(Absorptivity_Muscle*Z_Muscle-R_Muscle.^2)./(2*sigma^2);

figure
mesh(R_Dermis,Z_Dermis,Q_Dermis)
hold on;
#figure
mesh(R_Fat,Z_Fat,Q_Fat)
#hold on;
#figure
#mesh(R_Muscle,Z_Muscle,Q_Muscle)
