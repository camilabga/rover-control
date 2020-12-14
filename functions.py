from matplotlib.widgets import Slider
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def w_dot(Uv, Ud, w, K, i, J):
    dot = (-1*Uv*w - Ud*np.sign(w) + K*i)/J
    return dot

def rungeKutta(w0, dt, Uv, Ud, K, i, J):
    # Count number of iterations using step size or
    # step height h
    # Iterate for number of iterations

    "Apply Runge Kutta Formulas to find next value of y"
    k1 = dt * w_dot(Uv, Ud, w0, K, i, J)
    k2 = dt * w_dot(Uv, Ud, w0 + 0.5 * k1, K, i, J)
    k3 = dt * w_dot(Uv, Ud, w0 + 0.5 * k2, K, i, J)
    k4 = dt * w_dot(Uv, Ud, w0 + k3, K, i, J)

    # Update next value of y
    w = w0 + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    return w

def generate_values(tf, W, Wd, _lambda, J, K, Ud, Uv, n=1):
    _w = []
    _e = []
    _i = []
    t = tf*1000-1
    e = W - Wd
    i = J * (-1 * _lambda * e) / K
    while t > 0:
        for f in range(n):
            _w.append(W)  ### saves in a list the next value of w
            _e.append(e)  ### save the error to plot later
            _i.append(i)
            W = rungeKutta(W, 0.001, Uv, Ud, K, i, J)
            e = W - Wd
            t = t - 1
            if t < 0:
                break
        i = J * (-1 * _lambda * e) / K  ### calculates the current
    if n == 1:
        _w.append(W)
        _e.append(W - Wd)
        _i.append(J * (-1 * _lambda * e) / K)
    return _w, _e, _i

def plot_dinamic(lambda0, w0, Wd0, Ud0, Uv0, tf, J, K):
    # General plot parameters
    mpl.rcParams['font.family'] = 'DejaVu Sans'
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.linewidth'] = 2
    mpl.rcParams['axes.spines.top'] = False
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['xtick.major.size'] = 5
    mpl.rcParams['xtick.major.width'] = 2
    mpl.rcParams['ytick.major.size'] = 5
    mpl.rcParams['ytick.major.width'] = 2

    # Create figure and add axes
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111)
    fig.subplots_adjust(bottom=0.2, top=0.70)
    ax.set_ylabel('W(rad/s)')
    ax.set_xlabel('Tempo(s)')

    # Create axes for sliders
    ax_lambda = fig.add_axes([0.3, 0.85, 0.4, 0.05])
    ax_lambda.spines['top'].set_visible(True)
    ax_lambda.spines['right'].set_visible(True)

    ax_Wd = fig.add_axes([0.3, 0.92, 0.4, 0.05])
    ax_Wd.spines['top'].set_visible(True)
    ax_Wd.spines['right'].set_visible(True)

    ax_Ud = fig.add_axes([0.3, 0.78, 0.4, 0.05])
    ax_Ud.spines['top'].set_visible(True)
    ax_Ud.spines['right'].set_visible(True)

    ax_Uv = fig.add_axes([0.3, 0.71, 0.4, 0.05])
    ax_Uv.spines['top'].set_visible(True)
    ax_Uv.spines['right'].set_visible(True)

    # Create sliders
    s_lambda = Slider(ax=ax_lambda, label='Lambda ', valmin=-5, valmax=5,
                  valinit=lambda0, valfmt='%f', facecolor='#cc7000')
    s_Wd = Slider(ax=ax_Wd, label='Wd', valmin=-50, valmax=50,
                 valinit=Wd0, valfmt='%f rad/s', facecolor='#cc7000')
    s_Ud = Slider(ax=ax_Ud, label='Ud', valmin=-0.001, valmax=0.001,
                 valinit=Ud0, valfmt='%f', facecolor='#cc7000')
    s_Uv = Slider(ax=ax_Uv, label='Uv', valmin=-0.001, valmax=0.001,
                 valinit=Uv0, valfmt='%f', facecolor='#cc7000')

    # Generate default data
    _w, _e, _i = generate_values(tf,w0,Wd0,lambda0,J,K, Ud0, Uv0)
    # Plot default data
    _t = list(np.linspace(0,tf,1000*tf))
    f_d, = ax.plot(_t, _w, linewidth=2.5)
    wd_line, = ax.plot(_t, [Wd0]*len(_t), c='r',linewidth=2.5)

    fig2 = plt.figure(figsize=(20, 20))
    ax2 = fig2.add_subplot(111)
    f_d2, = ax2.plot(_t, _e, linewidth=2.5)
    ax2.set_ylabel('Erro (rad/s)')
    ax2.set_xlabel('Tempo(s)')

    fig3 = plt.figure(figsize=(20, 20))
    ax3 = fig3.add_subplot(111)
    f_d3, = ax3.plot(_t, _i, linewidth=2.5)
    ax3.set_ylabel('Corrente i (A)')
    ax3.set_xlabel('Tempo(s)')

    # Update values
    def update(val):
        _lambda = s_lambda.val
        Wd = s_Wd.val
        Ud = s_Ud.val
        Uv = s_Uv.val

        _w, _e, _i = generate_values(tf, w0, Wd, _lambda, J, K, Ud, Uv)

        wd_line.set_data(_t, [Wd]*len(_t))
        f_d.set_data(_t,_w)
        f_d2.set_data(_t,_e)
        f_d3.set_data(_t, _i)
        fig.canvas.draw_idle()
        fig2.canvas.draw_idle()
        fig3.canvas.draw_idle()

    s_lambda.on_changed(update)
    s_Uv.on_changed(update)
    s_Ud.on_changed(update)
    s_Wd.on_changed(update)

    plt.show()

def plot_series(lambda0, w0, Wd0, Ud0, Uv0, tf, J, K):
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
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)

    # Get colors from coolwarm colormap
    colors = plt.get_cmap('coolwarm', 10)

    lambda_values = [0.1, 0.2, 0.3, 0.4, 0.5, 1, 2, 3, 4, 5]

    for i in range(len(lambda_values)):
        _t = list(np.linspace(0, tf, 1000 * tf))
        _w, _e, _i = generate_values(tf, w0, Wd0, lambda_values[i], J, K, Ud0, Uv0)
        ax.plot(_t, _i, color=colors(i), linewidth=2.5)

    # wd_line, = ax.plot(_t, [Wd0] * len(_t), c='r', linewidth=2.5)

    # Add legend
    labels = ['Lambda = 0.1', 'Lambda = 0.2', 'Lambda = 0.3', 'Lambda = 0.4',
              'Lambda = 0.5', 'Lambda = 1', 'Lambda = 2', 'Lambda = 3',
              'Lambda = 4', 'Lambda = 5']
    ax.legend(labels, loc='upper right',
              frameon=False, labelspacing=0.2)
    ax.set_ylabel('Corrente (A)')
    ax.set_xlabel('Tempo(s)')

    ### Ud

    fig1 = plt.figure(figsize=(6, 4))
    ax1 = fig1.add_subplot(111)

    ud_values = [0, 0.0001, 0.0005, 0.001]

    for i in range(len(ud_values)):
        _t = list(np.linspace(0, tf, 1000 * tf))
        _w, _e, _i = generate_values(tf, w0, Wd0, lambda0, J, K, ud_values[i], Uv0)
        ax1.plot(_t, _i, color=colors(i), linewidth=2.5)

    # wd_line, = ax1.plot(_t, [Wd0] * len(_t), c='r', linewidth=2.5)

    # Add legend
    labels = ['Ud = 0', 'Ud = 0.0001', 'Ud = 0.0005',
              'Ud = 0.001']
    ax1.legend(labels, loc='upper right',
              frameon=False, labelspacing=0.2)
    ax1.set_ylabel('Corrente (A)')
    ax1.set_xlabel('Tempo(s)')

    ### Uv

    fig2 = plt.figure(figsize=(6, 4))
    ax2 = fig2.add_subplot(111)

    uv_values = [0, 0.00001, 0.00005, 0.0001]

    for i in range(len(uv_values)):
        _t = list(np.linspace(0, tf, 1000 * tf))
        _w, _e, _i = generate_values(tf, w0, Wd0, lambda0, J, K, Ud0, uv_values[i])
        ax2.plot(_t, _i, color=colors(i), linewidth=2.5)

    # wd_line, = ax2.plot(_t, [Wd0] * len(_t), c='r', linewidth=2.5)

    # Add legend
    labels = ['Uv = 0', 'Uv = 0.00001', 'Uv = 0.00005',
              'Uv = 0.0001']
    ax2.legend(labels, loc='upper right',
               frameon=False, labelspacing=0.2)
    ax2.set_ylabel('Corrente (A)')
    ax2.set_xlabel('Tempo(s)')

    ax.title.set_text("Comportamento da corrente com a variação de Lambda")
    ax1.title.set_text("Comportamento da corrente com a variação de Ud")
    ax2.title.set_text("Comportamento da corrente com a variação de Uv")

    plt.show()

def plot_frequency(lambda0, w0, Wd0, Ud0, Uv0, tf, J, K, n):
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
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)

    # Get colors from coolwarm colormap
    colors = plt.get_cmap('coolwarm', 10)

    n_values = [1, 10, 100, 500, 1000, 2000, 2500, 5000]#, 7500, 10000, 15000]

    for i in range(len(n_values)):
        _t = list(np.linspace(0, tf, 1000 * tf))
        _w, _e, _i = generate_values(tf, w0, Wd0, lambda0, J, K, Ud0, Uv0, n_values[i])
        ax.plot(_t, _w, color=colors(i), linewidth=2.5)

    wd_line, = ax.plot(_t, [Wd0] * len(_t), c='r', linewidth=2.5)

    # Add legend
    labels = ['n = 1x', 'n = 10x', 'n = 100x', 'n = 500x',
              'n = 1000x', 'n = 2000x', 'n = 2500x', 'n = 5000x']
    ax.legend(labels, loc='upper right',
              frameon=False, labelspacing=0.2)
    ax.set_ylabel('Velocidade angular (Rad/s)')
    ax.set_xlabel('Tempo(s)')

    ax.title.set_text("Comportamento da velocidade angular com a variação da frequência da ação de controle (n)")

    plt.show()

    return 0
