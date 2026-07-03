import numpy as np
# import scipy as sc
import matplotlib.pyplot as plt
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


if __name__ == '__main__':
    print('oskour')
