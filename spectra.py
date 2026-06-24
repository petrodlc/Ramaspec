import numpy as np
import scipy as sc


class spectra:
    __name = ''
    __data = np.full(0, None)
    __bkg_params = np.full((0, 2, 0), 0)
    __fit_params = np.full((8, 2, 0), 0)
    __mean_data = np.full(0, None)
    __mean_bkg_params = np.full(0, None)
    __mean_fit_params = np.full(0, None)
    __xoffset = np.zeros(0)
    __norm = np.ones(0)

    def __init__(self,
                 name='',
                 files=[]):
        self.__name = str(name)
        if len(files) != 0:
            self.read_from_files(files)
        return None

# #############################################################################
# ####################### GETTERS / SETTERS / DELETERS ########################
# #############################################################################

    @property
    def name(self):
        return self.__name

    @property
    def data(self):
        return self.__data.copy()

    @property
    def shift(self):
        return self.__data[:, 0, :].copy()

    @property
    def count(self):
        return self.__data[:, 1, :].copy()

    @property
    def bkg(self):
        return self.__data[:, 2, :].copy()

    @property
    def fit(self):
        return self.__lbwf(self.__data[:, 0, :], self.__fit_params[:, 0])

    @property
    def mean_data(self):
        return self.__mean_data.copy()

    @property
    def mean_shift(self):
        return self.__mean_data[:, 0, :].copy()

    @property
    def mean_count(self):
        return self.__mean_data[:, 1, :].copy()

    @property
    def mean_bkg(self):
        return self.__mean_data[:, 2, :].copy()

    @property
    def mean_fit(self):
        return self.__lbwf(
                self.__mean_data[:, 0, 0],
                self.__mean_fit_params[:, 0]
                )

    @property
    def bkg_params(self):
        return self.__bkg_params.copy()

    @property
    def fit_params(self):
        return self.__fit_params.copy()

    @property
    def mean_bkg_params(self):
        return self.__mean_bkg_params.copy()

    @property
    def mean_fit_params(self):
        return self.__mean_fit_params.copy()

    @property
    def xoffset(self):
        return self.__xoffset.copy()

    @property
    def norm(self):
        return self.__norm.copy()

# #############################################################################

    @name.setter
    def name(self, name):
        self.name = str(name)
        return

    @data.setter
    def data(self, data):
        data_temp = np.array(data, copy=True)
        if len(data.shape) != 3 or data.shape[1] != 3:
            # OSKOUR
            raise ValueError
        self.__data = data_temp
        del self.bkg_params
        del self.fit_params
        del self.mean_data
        del self.mean_bkg_params
        del self.mean_fit_params
        del self.xoffset
        del self.norm
        return

# #############################################################################

    @name.deleter
    def name(self):
        self.__name = ''
        return

    @data.deleter
    def data(self):
        self.__data = np.full((0, 3, 0), None)
        del self.bkg_params
        del self.fit_params
        del self.mean_data
        del self.mean_bkg_params
        del self.mean_fit_params
        del self.xoffset
        del self.norm
        return

    @bkg_params.deleter
    def bkg_params(self):
        self.__bkg_params = np.full((4, 2, self.__data.shape[2]), None)
        return

    @fit_params.deleter
    def fit_params(self):
        self.__fit_params = np.full((8, 2, self.__data.shape[2]), None)
        return

    @mean_data.deleter
    def mean_data(self):
        self.__mean_data = np.full((self.__data.shape[0], 3, 2), None)
        return

    @mean_bkg_params.deleter
    def mean_bkg_params(self):
        self.__mean_bkg_params = np.full((4, 2, 2), None)
        return

    @mean_fit_params.deleter
    def mean_fit_params(self):
        self.__mean_fit_params = np.full((4, 2, 2), None)
        return

    @xoffset.deleter
    def xoffset(self):
        self.__xoffset = np.zeros(self.__data.shape[2])
        return

    @norm.deleter
    def norm(self):
        self.__norm = np.ones(self.__data.shape[2])
        return

# #############################################################################
# ################################# METHODS ###################################
# #############################################################################

    def __polyfit(self, x, p):
        return np.sum([p[i] * x**i for i in range(len(p))], axis=0)

    def __lorentz(self, x, p):
        # x: w; p: [w_max, I_max, fwhm]
        np.array(p, copy=True).resize(3)
        return p[1] * (p[2] / 2)**2 / ((x - p[0])**2 + (p[2] / 2)**2)

    def __bwf(self, x, p):
        # x: w; p: [w_max, I_max, fwhm, Q]
        np.array(p, copy=True).resize(4)
        return p[1] * (1 + (2 * (x - p[0]) / (p[3] * p[2])))**2 / \
            (1 + (2 * (x - p[0]) / p[2])**2)

    def __lbwf(self, x, p):
        # x: w; p: [w_bwf, I_bwf, fwhm_bwf, Q_bwf, w_l, I_l, fwhm_l, offset]
        np.array(p, copy=True).resize(8)
        return self.__bwf(x, p[:4]) + self.__lorentz(x, p[4:7]) + p[7]

    def read_from_files(self, files, mode='t', rename=None):
        if mode == 'b':
            # OSKOUR
            raise NotImplementedError
        if mode != 't':
            # OSKOUR
            raise ValueError
        data_tot = []
        for file in np.atleast_1d(files):
            with open(file, 'rt', encoding='utf-8') as f:
                sep_data = np.array(
                        [[float(v) for v in line.split()] for line in f]
                        )
            if not sep_data.size:
                # OSKOUR
                continue
            if len(sep_data.shape) == 1 or sep_data.shape[1] == 1:
                data = np.concatenate(
                        (
                            np.atleast_2d(sep_data).transpose(1, 0),
                            np.zeros((sep_data.shape[0], 2))
                            ),
                        axis=1
                        )
            elif sep_data.shape[1] >= 3:
                data = sep_data[:, :3]
            else:
                data = np.concatenate(
                        (
                            sep_data,
                            np.zeros((sep_data.shape[0],
                                      3 - sep_data.shape[1]))
                            ),
                        axis=1
                        )
            data_tot.append(data)
        self.data = np.array(data_tot).transpose(1, 2, 0)
        if rename is not None:
            self.__name = str(rename)
        return

    def shift_x(self, xoffset):
        n_spc = self.__data.shape[2]
        if np.atleast_1d(xoffset).shape[0] != n_spc:
            xoffset = np.full(n_spc, np.atleast_1d(xoffset)[0])
        for i in range(n_spc):
            self.__data[:, 0, i] += xoffset[i]
        self.__xoffset += xoffset
        return

    def set_range(self, inf, sup):
        inf_id, sup_id = self.get_index([inf, sup])[0]
        if inf_id == sup_id:
            # OSKOUR
            return
        self.__data = self.__data[inf_id:sup_id + 1, :, :]
        self.__mean_data = self.__mean_data[inf_id:sup_id, :, :]
        return

    def remove_bkg_poly(self, inf, sup, ord=3, p0=None):
        if p0 is None:
            p0 = np.ones(ord + 1)
        params = []
        for i in range(self.__data.shape[2]):
            inf_id, sup_id = self.get_index([inf, sup], spc=i)[0]
            bkg_data = np.concatenate((
                self.__data[:inf_id + 1, :, i],
                self.__data[sup_id:, :, i]
                ))

            popt, pcov = sc.optimize.curve_fit(
                    lambda x, *args: self.__polyfit(x, args),
                    bkg_data[:, 0],
                    bkg_data[:, 1],
                    p0=p0
                    )
            perr = np.sqrt(np.diag(pcov))

            bkg = self.__polyfit(self.shift[:, i], popt)
            self.__data[:, 1, i] -= bkg
            self.__data[:, 2, i] += bkg
            params.append([popt, perr])
        self.__bkg_params = np.transpose(params, (2, 1, 0))
        return

    def normalize(self):
        class_width = (self.__data[-1, 0, :] - self.data[0, 0, :]) \
                / (self.__data.shape[0] + 1)
        self.__norm = np.linalg.norm(self.__data[:, 1, :], axis=0, ord=2) \
            * class_width

        self.__data[:, [1, 2], :] /= self.__norm
        self.__bkg_params[:, 0, :] /= self.__norm
        self.__bkg_params[:, 1, :] = abs(
                self.__bkg_params[:, 1, :] / self.__norm
                )
        # normalize mean ?
        return

    def fit_lbwf(self, p0=np.ones(8), fit_range=None):
        fit_range = np.atleast_1d(fit_range)
        if fit_range.shape == (2,):
            fit_range_id = np.array(self.get_index(fit_range)[0])
        else:
            if fit_range is not None:
                # OSKOUR
                pass    # for now
            fit_range_id = np.array([0, self.__data.shape[0] - 1])

        data_red = self.__data[fit_range_id[0]:fit_range_id[1] + 1, :, :]
        params = []
        for spc in data_red.transpose(2, 0, 1):
            popt, pcov = sc.optimize.curve_fit(
                    lambda x, *args: self.__lbwf(x, args),
                    spc[:, 0],
                    spc[:, 1],
                    p0=p0
                    )
            perr = np.sqrt(np.diag(pcov))
            params.append([popt, perr])
        self.__fit_params = np.transpose(params, (2, 1, 0))
        return

    def compute_mean_data(self):
        self.__mean_data = np.concatenate(
                np.atleast_3d(
                    self.__data.mean(axis=2),
                    self.__data.std(axis=2)
                    ),
                axis=2
                )
        return

    def compute_mean_bkg_params(self):
        self.__mean_bkg_params = np.concatenate(
                np.atleast_2d(
                    self.__bkg_params[:, 0, :].mean(axis=1),
                    (self.__bkg_params[:, 1, :]**2).sum(axis=1)
                    )
                ).transpose(1, 0)
        return

    def compute_mean_fit_params(self):
        self.__mean_fit_params = np.concatenate(
                np.atleast_2d(
                    self.__fit_params[:, 0, :].mean(axis=1),
                    (self.__fit_params[:, 1, :]**2).sum(axis=1)
                    )
                ).transpose(1, 0)
        return

    def get_index(self, values, spc=0, col=0):
        arr = self.__data[:, col, spc]
        n = len(values)
        indices = np.zeros(n, dtype=np.int64)
        diffs = np.array([arr[0] - v for v in values])
        for i in range(1, arr.size):
            val = arr[i]
            for j in range(n):
                diff = val - values[j]
                if abs(diff) < abs(diffs[j]):
                    indices[j], diffs[j] = i, diff
        return indices, diffs
