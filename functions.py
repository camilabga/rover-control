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

def generate_values(tf, W, Wd, _lambda, J, K, Ud, Uv):
    _w = [W]
    _e = []
    for t in range(tf*1000-1):
        e = W - Wd
        _e.append(e)  ### save the error to plot later
        i = J * (-1 * _lambda * e) / K  ### calculates the current
        W = rungeKutta(W, 0.001, Uv, Ud, K, i, J)
        _w.append(W)  ### saves in a list the next value of w
    _e.append(W - Wd)
    return _w, _e

def plot(lambda0, w0, Wd0, Ud0, Uv0, tf, J, K):
    # General plot parameters
    mpl.rcParams['font.family'] = 'DejaVu Sans'
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.linewidth'] = 2
    mpl.rcParams['axes.spines.top'] = False
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['xtick.major.size'] = 10
    mpl.rcParams['xtick.major.width'] = 2
    mpl.rcParams['ytick.major.size'] = 10
    mpl.rcParams['ytick.major.width'] = 2

    # Create figure and add axes
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111)
    fig.subplots_adjust(bottom=0.2, top=0.70)

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
    _w, _e = generate_values(tf,w0,Wd0,lambda0,J,K, Ud0, Uv0)
    # Plot default data
    _t = list(np.linspace(0,tf,1000*tf))
    f_d, = ax.plot(_t, _w, linewidth=2.5)
    wd_line, = ax.plot(_t, [Wd0]*len(_t), c='r',linewidth=2.5)

    # Update values
    def update(val):
        _lambda = s_lambda.val
        Wd = s_Wd.val
        Ud = s_Ud.val
        Uv = s_Uv.val

        _w, _e = generate_values(tf, w0, Wd, _lambda, J, K, Ud, Uv)

        wd_line.set_data(_t, [Wd]*len(_t))
        f_d.set_data(_t,_w)
        fig.canvas.draw_idle()

    s_lambda.on_changed(update)
    s_Uv.on_changed(update)
    s_Ud.on_changed(update)
    s_Wd.on_changed(update)

    plt.show()