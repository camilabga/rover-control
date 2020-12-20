from functions03 import plot

##### set initial values #####
J = 0.0002
K = 0.04

tf = 50  ### tempo em seg

_lambda = 1
# 0.25 0.5 1
Wd = 25
w0 = 0

u_chapeu = 0

mi = 0.0005
# 0 0.0005 0.0001
plot(_lambda, w0, Wd, mi, tf, J, K, u_chapeu)