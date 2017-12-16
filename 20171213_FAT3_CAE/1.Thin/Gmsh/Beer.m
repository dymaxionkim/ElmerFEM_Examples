##########################################################
# Beer-Lambert Plot
# Heat Generation by LED Light through Human Skin Tissues
# 20171215 Dymaxionkim
##########################################################

Depth_Dermis = 0.0015;
Depth_Fat = 0.005;
Depth_Muscle = 0.020;
Width = 0.06;
Segment = 2000;

r = -Width/2:1/Segment:Width/2;
z_Dermis = -Depth_Dermis:1/Segment:0.0;
z_Fat = -(Depth_Dermis+Depth_Fat):1/Segment:-Depth_Dermis;
z_Muscle = -(Depth_Dermis+Depth_Fat+Depth_Muscle):1/Segment:-(Depth_Dermis+Depth_Fat);
z = [z_Dermis, z_Fat, z_Muscle];
[R,Z] = meshgrid(r,z);

I0 = 2.0; #[W/m^2], the irradiation intensity at the skin surface
sigma = 0.002; #[m], the width of the irradiated region (the standard deviation of the Gaussian function which describes the beam profile)
Ab_Dermis = 12; #[1/m]
Ab_Fat = 9; #[1/m]
Ab_Muscle = 30; #[1/m]

#Q_Dermis = I0*Ab_Dermis*exp(Ab_Dermis*Z(1:length(z_Dermis),:)-R(1:length(z_Dermis),:).^2/(2*sigma^2));
#Q_Fat = I0*Ab_Fat*exp(Ab_Fat*Z(length(z_Dermis)+1:length(z_Dermis)+length(z_Fat),:)-R(length(z_Dermis)+1:length(z_Dermis)+length(z_Fat),:).^2/(2*sigma^2));
#Q_Fat = Q_Fat - (Q_Fat(1,:)-Q_Dermis(size(Q_Dermis)(1),:));
#Q_Muscle = I0*Ab_Muscle*exp(Ab_Muscle*Z(length(z_Dermis)+length(z_Fat)+1:length(z_Dermis)+length(z_Fat)+length(z_Muscle),:)-R(length(z_Dermis)+length(z_Fat)+1:length(z_Dermis)+length(z_Fat)+length(z_Muscle),:).^2/(2*sigma^2));
#Q_Muscle = Q_Muscle - (Q_Muscle(1,:)-Q_Fat(size(Q_Fat)(1),:));
#Q = [Q_Dermis; Q_Fat; Q_Muscle];

Q = I0*Ab_Dermis*exp(Ab_Dermis*Z-R.^2/(2*sigma^2));

#figure
mesh(R,Z,Q)

