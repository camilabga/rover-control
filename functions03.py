from matplotlib.widgets import Slider
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def w_dot(w, K, i, J,mi):
    dot = (-mi*(w+np.sign(w)) + K*i)/J
    return dot

def rungeKutta(w0, dt, mi, K, i, J, u_chapeu):
    # Count number of iterations using step size or
    # step height h
    # Iterate for number of iterations

    "Apply Runge Kutta Formulas to find next value of y"
    k1 = dt * w_dot(w0, K, i, J, mi)
    k2 = dt * w_dot(w0 + 0.5 * k1, K, i, J, mi)
    k3 = dt * w_dot(w0 + 0.5 * k2, K, i, J, mi)
    k4 = dt * w_dot(w0 + k3, K, i, J, mi)

    # Update next value of y
    w = w0 + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    return w

def generate_values(tf, W, Wd, _lambda, J, K, mi, u_chapeu, N):
    _w = [W]
    _e = []
    _i = []
    _u_chapeu = [0]
    for t in range(tf*1000-1):
        e = W - Wd
        _e.append(e)  ### save the error to plot later
        i = (u_chapeu*(W+np.sign(W)) + J*(0-(_lambda*e))) / K  ### calculates the current
        _i.append(i)
        u_chapeu = u_chapeu - (N * e * (W + np.sign(W)) * 0.001)
        _u_chapeu.append(u_chapeu)
        W = rungeKutta(W, 0.001, mi, K, i, J, u_chapeu)
        _w.append(W)  ### saves in a list the next value of w
    _e.append(W - Wd)
    _i.append((u_chapeu*(W+np.sign(W)) + J*(0-(_lambda*e))) / K)
    return _w, _e, _i, _u_chapeu


def plot(lambda0, w0, Wd0, mi, tf, J, K, u_chapeu):
    # General plot parameters
    mpl.rcParams['font.family'] = 'Avenir'
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.linewidth'] = 2
    mpl.rcParams['axes.spines.top'] = False
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['xtick.major.size'] = 10
    mpl.rcParams['xtick.major.width'] = 2
    mpl.rcParams['ytick.major.size'] = 10
    mpl.rcParams['ytick.major.width'] = 2

    # Create figure and add axes
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)

    fig1 = plt.figure(figsize=(12, 8))
    ax1 = fig1.add_subplot(111)

    fig2 = plt.figure(figsize=(12, 8))
    ax2 = fig2.add_subplot(111)

    # Get colors from coolwarm colormap
    colors = plt.get_cmap('twilight_shifted', 7)

    N_values = [0, 0.000000001, 0.00000001, 0.000000025, 0.00000005, 0.0000001, 0.000001]
    mi_values = [0, 0.000001, 0.000005, 0.00001, 0.0001, 0.001]

    # for i in range(len(mi_values)):
    for i in range(len(N_values)):
        _t = list(np.linspace(0, tf, 1000 * tf))
        _w, _e, _i, _u_chapeu = generate_values(tf, w0, Wd0, lambda0, J, K, mi, u_chapeu, N_values[i])
        # _w, _e, _i, _u_chapeu = generate_values(tf, w0, Wd0, lambda0, J, K, mi_values[i], u_chapeu, N)

        ax.plot(_t, _w, color=colors(i), linewidth=2.5)
        ax1.plot(_t, _i, color=colors(i), linewidth=2.5)
        ax2.plot(_t, _u_chapeu, color=colors(i), linewidth=2.5)

    wd_line, = ax.plot(_t, [Wd0] * len(_t), c='r', linewidth=2.5)

    # Add legend
    labels = ['n = 0','n = 10^(-9)', 'n = 10^(-8)', 'n = 25*10^(-8)','n = 5*10^(-8)', 'n = 10^(-7)', 'n = 10^(-6)']


    ax.legend(labels, loc='upper right',
              frameon=False, labelspacing=0.2)
    ax.set_ylabel('Velocidade angular (Rad/s)')
    ax.set_xlabel('Tempo(s)')

    ax.title.set_text("Comportamento da velocidade angular com a variação da taxa de adaptação (n)")
    ax1.title.set_text("Comportamento da corrente com a variação da taxa de adaptação (n)")
    ax2.title.set_text("Comportamento de coeficiente de atrito estimado com a variação da taxa de adaptação (n)")

    ax1.legend(labels, loc='upper right',
               frameon=False, labelspacing=0.2)
    ax1.set_ylabel('Corrente (A)')
    ax1.set_xlabel('Tempo(s)')

    ax2.legend(labels, loc='upper right',
               frameon=False, labelspacing=0.2)
    ax2.set_ylabel('Coeficiente de atrito estimado (u_chapeu)')
    ax2.set_xlabel('Tempo(s)')


    plt.show()

    return 0



