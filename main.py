import numpy as np
# import scipy as sc
import matplotlib.pyplot as plt
import scipy
import odrpack
# import pathlib as pth

import spectra as sp
from constants import p0, files, files_c, files_cs, xoffsets, classed, spc


def preprocess(s: sp.spectra, xoffset: float):
    s.shift_x(520.7 - xoffset)
    s.remove_bkg_poly(1100, 1900)
    s.normalize()
    return


def compute_data(s: sp.spectra):
    s.fit_lbwf(p0=p0, fit_range=[900, 2100])
    s.compute_mean_data()
    s.compute_mean_bkg_params()
    s.compute_mean_fit_params()
    return


def get_all():
    return [sp.spectra(name=name, files=files[name]) for name in files.keys()]


def process_dict(spc):
    for t in spc.keys():
        for name, s in spc[t].items():
            preprocess(s, xoffsets[name])
            compute_data(s)


def cmp_params(spc,
               xparam, yparam,
               xdiv=None, ydiv=None,
               err=2,
               src: (str, str) = None):
    params = {'G peak': [[], [], '(cm^-1)'],
              'Ig': [[], [], '(a. u.)'],
              'FWHMg': [[], [], '(cm^-1)'],
              '1/Q': [[], [], ''],
              'D peak': [[], [], '(cm^-1)'],
              'Id': [[], [], '(a. u.)'],
              'FWHMd': [[], [], '(cm^-1)'],
              'offset': [[], [], '(a. u.)'],
              'bkg0': [[], [], '(a. u.)'],
              'bkg1': [[], [], '(a. u. * cm)'],
              'bkg2': [[], [], '(a. u. * cm^2)'],
              'bkg3': [[], [], '(a. u. * cm^3)']}
    color = {'CI': 'blue', 'CM': 'orange', 'CR': 'gray'}
    legend_entries = [
            plt.Line2D([0], [0],
                       color=color[t],
                       linestyle='none',
                       marker='+',
                       markersize=10,
                       label=t)
            for t in ['CI', 'CM', 'CR']
            ]
    for t in spc.keys():
        for name, s in spc[t].items():
            k = list(params.keys())
            for i in range(8):
                params[k[i]][0].append(s.mean_fit_params[i])
                params[k[i]][1].append([name, t])
            for i in range(4):
                params[k[i + 8]][0].append(s.mean_bkg_params[i])
                params[k[i + 8]][1].append([name, t])
    for p in params.keys():
        params[p][0] = np.array(params[p][0])
        params[p][1] = np.array(params[p][1])
    px = params[xparam]
    if xdiv is not None:
        divx = params[xdiv]
    py = params[yparam]
    if ydiv is not None:
        divy = params[ydiv]
    ax = plt.axes([0.05, 0.05, 0.99 - 0.05, 0.95 - 0.05])
    for j in range(px[0].shape[0]):
        if xdiv is None:
            x = px[0][j, 0]
            xerr = px[0][j, err]
        else:
            x = px[0][j, 0] / divx[0][j, 0]
            xerr = np.abs(x) \
                * np.sqrt((px[0][j, err] / px[0][j, 0])**2
                          + (divx[0][j, err] / divx[0][j, 0])**2)
        if ydiv is None:
            y = py[0][j, 0]
            yerr = py[0][j, err]
        else:
            y = py[0][j, 0] / divy[0][j, 0]
            yerr = np.abs(y) \
                * np.sqrt((py[0][j, err] / py[0][j, 0])**2
                          + (divy[0][j, err] / divy[0][j, 0])**2)
        ax.errorbar(x, y, xerr=xerr, yerr=yerr,
                    color=color[px[1][j, 1]], marker='none')
        ax.annotate(px[1][j, 0], (x, y),
                    xytext=(0.5, 0.5),
                    textcoords='offset fontsize',
                    color=color[px[1][j, 1]])
    ax.minorticks_on()
    ax.ticklabel_format(style='sci',
                        axis='both',
                        scilimits=(0, 0),
                        useMathText=True)
    ax.grid(alpha=0.5, which='major')
    ax.grid(alpha=0.1, which='minor')
    ax.legend(handles=legend_entries)
    ax.set_title('Parameters comparison'
                 + ('' if src is None
                    else f' from {src[0]}, {src[1]} spectrums'))
    ax.set_xlabel(
            xparam
            + ((' ' + px[2] if px[2] != '' else '') if xdiv is None
               else ' / ' + xdiv
               + ('' if px[2] == divx[2]
                  else (f' ({px[2][1:-1]} / {divx[2][1:-1]})'
                        if px[2] != '' and divx[2] != ''
                        else f' {px[2]}{divx[2]}'))))
    ax.set_ylabel(
            yparam
            + ((' ' + py[2] if py[2] != '' else '') if ydiv is None
               else ' / ' + ydiv
               + ('' if py[2] == divy[2]
                  else (f' ({py[2][1:-1]} / {divy[2][1:-1]})'
                        if py[2] != '' and divy[2] != ''
                        else f' {py[2]}{divy[2]}'))))
    plt.get_current_fig_manager().full_screen_toggle()
    plt.show()
    return


def plot_params(spc_dict, err=2, src: (str, str) = None, caps=False):
    params = {'G peak': [[], []],
              'Ig': [[], []],
              'FWHMg': [[], []],
              '1/Q': [[], []],
              'D peak': [[], []],
              'Id': [[], []],
              'FWHMd': [[], []],
              'offset': [[], []],
              'bkg0': [[], []],
              'bkg1': [[], []],
              'bkg2': [[], []],
              'bkg3': [[], []]}
    color = {'CI': 'blue', 'CM': 'orange', 'CR': 'gray'}
    legend_entries = [
            plt.Line2D([0], [0], color=color['CI'], marker='|', label='CI'),
            plt.Line2D([0], [0], color=color['CM'], marker='|', label='CM'),
            plt.Line2D([0], [0], color=color['CR'], marker='|', label='CR')
            ]
    for t in spc_dict.keys():
        for s in spc_dict[t].values():
            k = list(params.keys())
            for i in range(8):
                params[k[i]][0].append(s.mean_fit_params[i])
                params[k[i]][1].append(t)
            for i in range(4):
                params[k[i + 8]][0].append(s.mean_bkg_params[i])
                params[k[i + 8]][1].append(t)
    for p in params.keys():
        params[p][0] = np.array(params[p][0])
        params[p][1] = np.array(params[p][1])
    ax = plt.axes([0.05, 0.05, 0.99 - 0.05, 0.95 - 0.05])
    for i in range(len(k)):
        p = params[k[i]]
        x_min = np.min(p[0][:, 0] - p[0][:, err])
        x_max = np.max(p[0][:, 0] + p[0][:, err])
        norm = 1 / (x_max - x_min)
        ax.plot([0, 1], [i] * 2, 'black',
                linestyle='none', marker='|', markersize=15, alpha=0.4)
        ax.annotate(f'{x_min:.2e}',
                    (0, i), xytext=(0, -15), textcoords='offset points',
                    ha='center', alpha=0.4)
        if i != len(k) - 1:
            ax.annotate(f'{x_max:.2e}',
                        (1, i), xytext=(0, -15), textcoords='offset points',
                        ha='center', alpha=0.4)
        else:
            ax.annotate(f'{x_max:.2e}',
                        (1, i), xytext=(0, -15), textcoords='offset points',
                        ha='right', alpha=0.4)
        if x_min * x_max < 0:
            ax.plot([-x_min * norm], [i], 'black',
                    marker='|', markersize=15, alpha=0.4)
            ax.annotate('0',
                        (-x_min * norm, i),
                        xytext=(0, 15), textcoords='offset points',
                        ha='center', alpha=0.4)
        for j in range(p[0].shape[0]):
            x = (p[0][j, 0] - x_min) * norm
            y = i
            xerr = p[0][j, err] * norm
            ax.errorbar(x, y, xerr=xerr, color=color[p[1][j]], fmt='none')
            ax.plot(x, y, color=color[p[1][j]], marker='|')
            if caps:
                ax.plot(x - xerr, y,
                        color=color[p[1][j]], marker='4', markersize=10)
                ax.plot(x + xerr, y,
                        color=color[p[1][j]], marker='3', markersize=10)
            # ax.errorbar(x, y, xerr=xerr, color=color[p[1][j]], marker='|')
    ax.set_xticks([])
    ax.set_yticks(np.arange(len(k)), labels=k)
    ax.grid(alpha=0.4)
    ax.legend(handles=legend_entries)
    ax.set_title('General parameters comparison'
                 + ('' if src is None
                    else f' from {src[0]}, {src[1]} spectrums'))
    ax.set_xlabel('Values (normalized)')
    plt.get_current_fig_manager().full_screen_toggle()
    plt.show()
    return


def lin_plot(spc, xpar, ypar, sigma=[1, 3, 5], classes=['CI', 'CM', 'CR'], err=2):
    params = {'G peak': [[], [], '(cm^-1)'],
              'Ig': [[], [], '(a. u.)'],
              'FWHMg': [[], [], '(cm^-1)'],
              '1/Q': [[], [], ''],
              'D peak': [[], [], '(cm^-1)'],
              'Id': [[], [], '(a. u.)'],
              'FWHMd': [[], [], '(cm^-1)'],
              'offset': [[], [], '(a. u.)'],
              'bkg0': [[], [], '(a. u.)'],
              'bkg1': [[], [], '(a. u. * cm)'],
              'bkg2': [[], [], '(a. u. * cm^2)'],
              'bkg3': [[], [], '(a. u. * cm^3)']}
    color = {'CI': 'blue', 'CM': 'orange', 'CR': 'gray'}
    legend_entries = [
            plt.Line2D([0], [0],
                       linestyle='none',
                       marker='+',
                       markersize=10,
                       color=color[t],
                       label=t)
            for t in spc.keys()
            ]
    for t in spc.keys():
        for name, s in spc[t].items():
            k = list(params.keys())
            for i in range(8):
                params[k[i]][0].append(s.mean_fit_params[i])
                params[k[i]][1].append([name, t])
            for i in range(4):
                params[k[i + 8]][0].append(s.mean_bkg_params[i])
                params[k[i + 8]][1].append([name, t])
    for p in params.keys():
        params[p][0] = np.array(params[p][0])
        params[p][1] = np.array(params[p][1])
    xparam = params[xpar]
    yparam = params[ypar]

    ax = plt.axes([0.05, 0.05, 0.99 - 0.05, 0.95 - 0.05])
    px = np.array([xparam[0][i]
                   for i in range(len(xparam[0]))
                   if xparam[1][i, 1] in classes])
    py = np.array([yparam[0][i]
                   for i in range(len(yparam[0]))
                   if yparam[1][i, 1] in classes])
    # [a, b], pcov = scipy.optimize.curve_fit(
    #         lambda x, a, b: a * x + b,
    #         px[:, 0],
    #         py[:, 0]
    #         )
    # aerr, berr = np.sqrt(np.diag(pcov))
    sol = odrpack.odr_fit(
            lambda x, p: p[0] + p[1] * x,
            px[:, 0],
            py[:, 0],
            beta0=[1.0, 0.0],
            weight_x=px[:, err]**-2,
            weight_y=py[:, err]**-2
            )
    b, a = sol.beta
    berr, aerr = sol.sd_beta
    print(
            f'a = {a} ± {aerr}'
            + (
                ''
                if xparam[2] == yparam[2]
                else (' ' + (
                    f'({yparam[2][1:-1]} / {xparam[2][1:-1]})'
                    if xparam[2] != '' and yparam[2] != ''
                    else (
                        yparam[2]
                        if yparam[2] != ''
                        else f'( 1 / {xparam[2][1:-1]})'
                        )
                    ))
                )
            )
    print(f'b = {b} ± {berr}' + (f' {yparam[2]}' if yparam[2] != '' else ''))

    for i in range(xparam[0].shape[0]):
        x = xparam[0][i, 0]
        y = yparam[0][i, 0] - a * x - b
        xerr = xparam[0][i, err]
        yerr = np.sqrt(yparam[0][i, err]**2
                       + a**2 * xerr**2
                       + x**2 * aerr**2 * 0
                       + berr**2 * 0)
        ax.errorbar(x, y,
                    xerr=xerr, yerr=yerr,
                    fmt='none', color=color[xparam[1][i, 1]])
        ax.annotate(xparam[1][i, 0],
                    (x, y),
                    xytext=(.5, .5),
                    textcoords='offset fontsize',
                    color=color[xparam[1][i, 1]])

    x_line = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 100)
    err_line = np.sqrt(x_line**2 * aerr**2 + berr**2)
    for sig in sigma:
        ax.fill_between(np.linspace(0, 1, 100),
                        sig * err_line,
                        -sig * err_line,
                        fc='black',
                        alpha=.15 / len(sigma),
                        transform=ax.get_yaxis_transform())

    ax.minorticks_on()
    ax.ticklabel_format(style='sci',
                        axis='both',
                        scilimits=(0, 0),
                        useMathText=True)
    ax.grid(alpha=.5, which='major')
    ax.grid(alpha=.1, which='minor')
    ax.legend(handles=legend_entries)
    ax.set_title('Parameters comparison')
    ax.set_xlabel(xpar + ((' ' + xparam[2]) if xparam[2] != '' else ''))
    ax.set_ylabel(
            f'{ypar} - ({a:.2e} * {xpar}'
            + (f' + {b:.2e})' if b >= 0 else f' - {-b:.2e})')
            + ((' ' + yparam[2]) if yparam[2] != '' else '')
            )
    plt.get_current_fig_manager().full_screen_toggle()
    plt.show()
    return


def mean_plot(s, sigma=[1, 3, 5], color='blue', alpha=.3):
    ax = plt.axes([0.05, 0.05, 0.99 - 0.05, 0.95 - 0.05])
    ax.set_xlim(s.mean_shift[0, 0], s.mean_shift[-1, 0])
    ax.set_title(f'{s.name} old mean (sigma = {sigma})')
    ax.set_xlabel('Raman shift (cm^-1)')
    ax.set_ylabel('Intensity (a. u.)')
    ax.minorticks_on()
    ax.grid(alpha=.5, which='major')
    ax.grid(alpha=.1, which='minor')
    plt.ticklabel_format(style='sci',
                         axis='y',
                         scilimits=(0, 0),
                         useMathText=True)
    ax.plot(s.mean_shift[:, 0], s.mean_count[:, 0], color)
    for sig in sigma:
        ax.fill_between(s.mean_shift[:, 0],
                        s.mean_count[:, 0] - sig * s.mean_count[:, 1],
                        s.mean_count[:, 0] + sig * s.mean_count[:, 1],
                        fc=color, alpha=alpha/len(sigma))
    plt.get_current_fig_manager().full_screen_toggle()
    plt.show()


def check_spc(spc):
    color = {'CI': 'blue', 'CM': 'orange', 'CR': 'gray'}
    marker = {'CI': '.', 'CM': '+', 'CR': 'x'}

    fig, axs = plt.subplots(2, 1)
    fig.subplots_adjust(left=.05,       # .05,
                        bottom=.05,     # .05,
                        right=.99,      # - .05,
                        top=.95,        # - .05,
                        hspace=.05,
                        wspace=0)
    axs[0].tick_params(top=False, labeltop=False, bottom=False, labelbottom=False)
    axs[0].tick_params(left=True, labelleft=True, right=False, labelright=False)
    axs[1].tick_params(top=False, labeltop=False, bottom=True, labelbottom=True)
    axs[1].tick_params(left=False, labelleft=False, right=False, labelright=False)
    axs[0].set_xticks([0, 1], labels=[])
    axs[0].set_yticks(np.arange(8))
    axs[1].set_yticks([0, 1], labels=[])
    axs[0].grid(alpha=.5)
    axs[1].grid(alpha=.5)
    axs[0].set_ylim(-.5, 7.5)
    axs[0].set_ylabel('Parameter index')
    axs[1].set_xlabel('Spectrum index')
    for t in ['CI']:    # spc.keys():
        for name, s in spc[t].items():
            fig.suptitle(name)
            axs[1].set_xticks(np.arange(s.fit_params.shape[2]))
            mean_p = s.mean_fit_params
            x_min = mean_p[:, 0] - mean_p[:, 2]
            x_max = mean_p[:, 0] + mean_p[:, 2]
            norm = 1 / (x_max - x_min)
            in_count = np.zeros(s.fit_params.shape[0::2])
            axs[0].fill_between([0, 1], [0] * 2, [1] * 2, fc=color[t], alpha=.1, transform=axs[0].get_xaxis_transform())
            axs[1].fill_between([0, 1], [0] * 2, [1] * 2, fc=color[t], alpha=.1, transform=axs[1].get_yaxis_transform())
            for j in range(s.fit_params.shape[2]):
                p = s.fit_params[:, :, j]
                for i in range(p.shape[0]):
                    axs[0].plot(norm[i] * (p[i, 0] - x_min[i]),
                                i,
                                color=color[t],
                                marker=marker[t],
                                linestyle='none')
                    axs[0].annotate(j,
                                    (norm[i] * (p[i, 0] - x_min[i]), i),
                                    xytext=(0, 1),
                                    textcoords='offset fontsize',
                                    ha='center',
                                    va='center')
                    if x_min[i] <= p[i, 0] <= x_max[i]:
                        in_count[i, j] = 1
                    axs[1].plot(j,
                                norm[i] * (p[i, 0] - x_min[i]),
                                color=color[t],
                                marker=marker[t],
                                linestyle='none')
                    axs[1].annotate(i,
                                    (j, norm[i] * (p[i, 0] - x_min[i])),
                                    xytext=(-1, 0),
                                    textcoords='offset fontsize',
                                    ha='center',
                                    va='center')
                axs[1].annotate(f'{100 * in_count[:, j].sum() / in_count.shape[0]:.0f}%',
                                (j, 0),
                                xytext=(0, .5),
                                xycoords=axs[1].get_xaxis_transform(),
                                textcoords='offset fontsize',
                                ha='center',
                                va='bottom',
                                backgroundcolor='white')
            for i in range(s.fit_params.shape[0]):
                axs[0].annotate(f'{100 * in_count[i, :].sum() / in_count.shape[1]:.0f}%',
                                (0, i),
                                xytext=(.5, 0),
                                xycoords=axs[0].get_yaxis_transform(),
                                textcoords='offset fontsize',
                                ha='left',
                                va='center',
                                backgroundcolor='white')
            # ######################

            def onclick(event):
                print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                      ('double' if event.dblclick else 'single',
                       event.button,
                       event.x, event.y,
                       event.xdata if event.xdata is not None else -1,
                       event.ydata if event.ydata is not None else -1))

            cid = fig.canvas.mpl_connect('button_press_event', onclick)
            # #####################
            plt.get_current_fig_manager().full_screen_toggle()
            plt.show()
            return

def test(spc):
    plt.get_current_fig_manager().window.state('zoomed')
    plt.show()
    process_dict(spc)
    check_spc(spc)


if __name__ == '__main__':
    test(spc)
