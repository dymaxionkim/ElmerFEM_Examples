r = -0.01:0.001:0.01;
z = -0.0095:0.001:0.0;
[R,Z] = meshgrid(r,z);

I0 = 0.002;
sigma = 0.005;
Absorptivity_Dermis = 12.0;
Absorptivity_Fat = 9.0;
Absorptivity_Muscle = 3.0;
Ab = Absorptivity_Dermis;

#Q = exp(-(R.^2+Z.^2))
Q = I0*Ab*exp(10*Ab*Z-100000*R.^2)./(2*sigma^2);
#Q = I0*Ab*exp(Ab*Z-R.^2)./(2*sigma^2);
#Q = I0.*Absorptivity_Dermis.*exp(Absorptivity_Dermis.*z-r.^2)./(2*sigma.^2);
mesh(R,Z,Q)
