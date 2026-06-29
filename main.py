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


if __name__ == '__main__':
    print('oskour')
