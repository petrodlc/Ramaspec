import numpy as np
# import scipy as sc
# import matplotlib.pyplot as plt
# import glob
import pathlib as pth

# from spectrum import spectrum

lbwf_ini = np.array([[1605, 300, 83, -7, 1352, 200, 121, 0]])
path = pth.Path(pth.Path.cwd().anchor) / 'Users' / 'petrodlc' / 'Documents' / \
        'Data' / 'LEW87022' / 'exports' / 'LEW87022_405_01_Points0.txt'

data_directory = path.parents[2]
files = {}
for meteorite in [
        'Ivuna',
        'Alais',
        'LEW87022',
        'MET01070',
        'GRA95229',
        'QUE99177'
        ]:
    directory = data_directory / meteorite / 'exports'
    files[meteorite] = sorted(directory.glob(meteorite + '_405_*.txt'))


def lorentz(w, w_max, fwhm, I_max):
    return I_max * (fwhm / 2)**2 / ((w - w_max)**2 + (fwhm / 2)**2)


def bwf(w, w_max, Q, fwhm, I_max):
    return I_max * (1 + (2 * (w - w_max) / (Q * fwhm))**2) / \
            (1 + (2 * (w - w_max) / fwhm)**2)


def lbwf(w, w_l, w_bwf, I_l, I_bwf, fwhm_l, fwhm_bwf, Q_bwf):
    return lorentz(w, w_l, fwhm_l, I_l) + bwf(w, w_bwf, Q_bwf, fwhm_bwf, I_bwf)


if __name__ == '__main__':
    print('oskour')
