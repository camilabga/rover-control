from functions import plot

##### set dos valores iniciais #####
J = 0.0002
K = 0.04

tf = 100  ### tempo em seg

_lambda = 0.1
Wd = 25
Ud = 0
Uv = 0
w0 = 0

plot(_lambda, w0, Wd, Ud, Uv, tf, J, K) ### plot the interactive graph