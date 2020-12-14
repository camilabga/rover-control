from functions import plot_series
from functions import plot_dinamic
from functions import plot_frequency

##### set initial values #####
J = 0.0002
K = 0.04

tf = 50  ### tempo em seg

_lambda = 0.3
Wd = 25
Ud = 0
Uv = 0
w0 = 0

n = 1

# plot_dinamic(_lambda, w0, Wd, Ud, Uv, tf, J, K) ### plot the interactive graph
# plot_series(_lambda, w0, Wd, Ud, Uv, tf, J, K) ### plot the serie graph
plot_frequency(_lambda, w0, Wd, Ud, Uv, tf, J, K, n) ###