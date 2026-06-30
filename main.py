import numpy as np
# import scipy as sc
import matplotlib.pyplot as plt
# import pathlib as pth

import spectra as sp
from constants import p0, files, files_c, files_cs, xoffsets, classed


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


def cmp_params(spc, xparam, yparam, xdiv=None, ydiv=None):
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
            xerr = px[0][j, 1]
        else:
            x = px[0][j, 0] / divx[0][j, 0]
            xerr = np.abs(x) \
                * np.sqrt((px[0][j, 1] / px[0][j, 0])**2
                          + (divx[0][j, 1] / divx[0][j, 0])**2)
        if ydiv is None:
            y = py[0][j, 0]
            yerr = py[0][j, 1]
        else:
            y = py[0][j, 0] / divy[0][j, 0]
            yerr = np.abs(y) \
                * np.sqrt((py[0][j, 1] / py[0][j, 0])**2
                          + (divy[0][j, 1] / divy[0][j, 0])**2)
        ax.errorbar(x, y, xerr=xerr, yerr=yerr,
                    color=color[px[1][j, 1]], marker='none')
        ax.annotate(px[1][j, 0], (x, y),
                    xytext=(0.5, 0.5),
                    textcoords='offset fontsize',
                    color=color[px[1][j, 1]])
    ax.minorticks_on()
    ax.grid(alpha=0.5, which='major')
    ax.grid(alpha=0.1, which='minor')
    ax.legend(handles=legend_entries)
    ax.set_title('Parameters comparison from old, strict spectrums')
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


if __name__ == '__main__':
    print('oskour')
