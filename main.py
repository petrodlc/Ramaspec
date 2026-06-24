import numpy as np
# import scipy as sc
# import matplotlib.pyplot as plt
import pathlib as pth
import spectra as sp

p0 = np.array([[1605, 5e-2, 83, -3e5, 1352, 3e-2, 121, 0]])
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


if __name__ == '__main__':
    print('oskour')
