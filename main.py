from functions import plot

##### set dos valores iniciais #####
J = 0.0002
K = 0.04

tf = 100 * 1000 ### tempo em ms

_lambda = 100
Wd = 50
Ud = 0
Uv = 0
w0 = 0

plot(_lambda, w0, Wd, Ud, Uv, tf, J, K) ### plot the interactive graph