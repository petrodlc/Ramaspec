A few python files that provide useful utilities to process Raman spectrums

# Installation

## Install
clone from GitHub:

```shell
git clone https://github.com/petrodlc/Ramaspec.git
```

## dependencies
- numpy
- scipy
- pathlib

## update

```shell
git pull
```

## Switching between versions

To switch to `dev` (unstable) version:
```shell
git checkout dev
```

and go back to stable:
```shell
git checkout main
```

## uninstall

remove directory
```shell
rm /path/to/directory
```

# Usage

import python files in your script, or from python console for live processing

```python
import spectra as sp
```

No ploting utility is currently added as matplotlib.pyplot works fine as is.
If you want a ploting utility, import this library as well :
```python
import matplotlib.pyplot as plt
```

For matplotlib usage, check its [documentation](https://matplotlib.org/stable/api/pyplot_summary.html#module-matplotlib.pyplot).

## spectra

/!\ This section will be moved to docstrings

This class is intended to store and process multiple spectrums.

### properties
#### get
All `numpy.ndarray` returned are *copies* of internal data stored.

- name: `str`, the name given to this spectra instance
- data: `numpy.ndarray` of shape (*n*, 3, *m*), where *n* is the length of the x axis and *m* is the number of individual spectrums.
It stores x axes (`data[:, 0, :]`), intensities (`data[:, 1, :]`), and background (`data[:, 2, :]`).
- shift, count and bkg: shorthands to get `data[:, 0, :]`, `data[:, 1, :]` and `data[:, 2, :]` respectively
- fit: fitted curve (`numpy.ndarray` of shape (*n*, *m*)). Computed from `shift` and `fit_params` on call.
- mean_data: `numpy.ndarray` of shape (*n*, 3, 2), where `mean_data[:, :, 0]` is the mean along the last axis of `data`, and `mean_data[:, :, 1]` is the standard deviation
- mean_shift, mean_count, mean_bkg and mean_fit: `numpy.ndarray` of shape (*n*, 2)
- bkg_params: `numpy.ndarray` of shape (*ord*, 2, *m*), where *ord* is the order of the polynome used to fit the baseline.
`bkg_params[:, 0, :]` are actual values of the parameters, while `bkg_params[:, 1, :]` are standard deviation.
- fit_params: `numpy.ndarray` of shape (8, 2, *m*), that stores the parameters of the fit (Breit-Wigner-Fano + Cauchy distribution + offset) alog with their standard deviation.
- mean_bkg_params and mean_fit_params: `numpy.ndarray` of shapes (*ord*, 2) and (8, 2), with mean parameters and errors computed from standard deviations.
- xoffset: `numpy.ndarray` of shape (*m*,), storing the correction made along the x axis.
Currently, all values should be equal, and an array is returned only for the sake of future development
- norm: `numpy.ndarray` of shape (*m*,), that stores the normalization factor (1 if none)

#### set
- name: a name to give to this spectra instance; should be `str`, but accepts anything with `__str__()` defined
- data: data to store (will be pass as a copy).
Should be convertible to `numpy.ndarray` of shape (*, 3, *).
Deletes `bkg_params`, `fit_params`, `mean_data`, `mean_bkg_params`, `mean_fit_params`, `xoffset` and `norm`, as they do not match anymore with new data.

#### delete
- name: back to empty string
- data: `numpy.ndarray` of shape (0, 3, 0), filled with `None`
Deletes `bkg_params`, `fit_params`, `mean_data`, `mean_bkg_params`, `mean_fit_params`, `xoffset` and `norm`, as they do not match anymore with empty data.
- bkg_params: `numpy.ndarray` of shape (0, 2, *m*) filled with `None`
- fit_params: `numpy.ndarray` of shape (8, 2, *m*) filled with `None`
- mean_data: `numpy.ndarray` of shape (*n*, 3, 2) filled with `None`
- mean_bkg_params: `numpy.ndarray` of shape (0, 2, 2) filled with `None`
- mean_fit_params: `numpy.ndarray` of shape (8, 2, 2) filled with `None`
- xoffset: `numpy.ndarray` of shape (*m*) filled with zeros
- norm: `numpy.ndarray` of shape (*m*) filled with ones
