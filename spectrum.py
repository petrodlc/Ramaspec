import numpy as np
import scipy as sc


class spectra:
    __name = ''
    __data = np.full(0, None)
    __mean_data = np.full(0, None)
    __bkg_fit = np.full(0, None)
    __bkg_params = np.full(0, None)
    __fit = np.full(0, None)
    __params = np.full(0, None)
    __mean_params = np.full(0, None)
    __shift_offset = np.zeros(0)
    __norm = np.zeros(0)

    def __init__(self, name=''):
        self.__name = str(name)
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
    def mean_data(self):
        return self.__mean_data.copy()

    @property
    def mean_params(self):
        return self.__mean_params.copy()

    @property
    def bkg_fit(self):
        return self.__bkg_fit.copy()

    @property
    def bkg_params(self):
        return self.__bkg_params.copy()

    @property
    def fit(self):
        return self.__fit.copy()

    @property
    def params(self):
        return self.__params.copy()

# #############################################################################

    @name.setter
    def name(self, name):
        self.__name = str(name)
        return self.__name

    @data.setter
    def data(self, data):
        data_temp = np.array(data, copy=True)
        if len(data.shape) != 3 and data.shape[1] != 3:
            msg = 'Data should be of shape (*, 3, *) ' \
                    f'(given is {data_temp.shape}).'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        self.__data = data_temp
        self.__shift_offset = np.zeros(self.__data.shape[0])
        return self.__data

# #############################################################################

    @name.deleter
    def name(self):
        save_name = self.__name
        self.__name = ''
        return save_name

# #############################################################################
# ################################# METHODS ###################################
# #############################################################################

    def read_from_files(self, files, mode='t', rename=''):
        if mode == 'b':
            msg = 'Reading file in \'b\' mode is not yet implemented. ' \
                    'Currently, only text, ' \
                    'space separated values are accepted.'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise NotImplementedError
        if mode != 't':
            msg = f'Unknown mode \'{mode}\'.'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        data_tot = []
        for file in np.atleast_1d(files):
            with open(file, 'rt', encoding='utf-8') as f:
                sep_data = np.array(
                        [[float(v) for v in line.split()] for line in f]
                        )
            if not sep_data.size:
                msg = f'Empty file \'{file}\' has been skipped.'
                print('[' + '\033[1m\033[33m' + 'WARNING' + '\033[0m' + ']> '
                      + msg)
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
        self.__data = np.array(data_tot).transpose(1, 2, 0)
        self.__shift_offset = np.zeros(self.__data.shape[0])
        if rename != '':
            self.__name = str(rename)
        return

    def shift_x(self, shift):
        spc = self.__data.shape[2]
        if np.atleast_1d(shift).shape[0] != spc:
            shift = np.full(spc, shift)
        for i in range(spc):
            self.__data[:, 0, i] += shift[i]
        if self.__shift_offset.shape[0] != spc:
            self.__shift_offset = shift
            return
        self.__shift_offset += shift
        return

    def set_range(self, inf, sup):
        inf_id, sup_id = map(int, self.get_index([inf, sup])[:, 0])
        if inf_id == sup_id:
            msg = f'Inf and sup idices are equal ({inf_id}). ' \
                    'Spectral range has not been modified.'
            print('[' + '\033[1m\033[33m' + 'WARNING' + '\033[0m' + ']> '
                  + msg)
            return
        self.__data = self.__data[inf_id:sup_id + 1, :, :]
        if self.__mean_data.size != 0:
            self.__mean_data = self.__mean_data[inf_id:sup_id + 1, :]
        return

    def compute_mean_data(self):
        self.__mean_data = np.concatenate(
                np.atleast_3d(
                    self.__data.mean(axis=2),
                    self.__data.std(axis=2)
                    ),
                axis=2
                )
        return self.__mean_data

    def compute_mean_params(self):
        self.__mean_params = self.__params.mean(axis=2)
        return self.__mean_params

    def remove_bkg_linear(self,
                          low_center,
                          top_center,
                          low_range,
                          top_range,
                          index=None):
        if index is None:
            data = self.__data.transpose(2, 0, 1)
        else:
            data = np.atleast_1d(self.__data.transpose(2, 0, 1)[index])
        bkg_fit = []
        bkg_params = []
        for sp in data:
            low = []
            top = []
            for i in range(sp.shape[0]):
                shift = sp[i, 0]
                if abs(shift - low_center) <= low_range * 0.5:
                    low.append([shift, sp[i, 1]])
                if abs(shift - top_center) <= top_range * 0.5:
                    top.append([shift, sp[i, 1]])
            low_anchor = np.array(low)
            top_anchor = np.array(top)
            low_anchor_mean = low_anchor.mean(axis=0)
            top_anchor_mean = top_anchor.mean(axis=0)

            slope = (top_anchor_mean[1] - low_anchor_mean[1]) / \
                    (top_anchor_mean[0] - low_anchor_mean[0])
            height = low_anchor_mean[1] - slope * low_anchor_mean[0]
            bkg_fit.append(lambda x, p: p[0] * x + p[1])
            bkg_params.append(np.array([slope, height]))
            sp[:, 2] = bkg_fit[-1](sp[:, 0], [slope, height])
            sp[:, 1] -= sp[:, 2]

        if index is None:
            self.__bkg_fit = np.array(bkg_fit)
            self.__bkg_params = np.array(bkg_params).transpose(1, 0)
            return

        nb_sp = self.__data.shape[2]
        if self.__bkg_fit.size != nb_sp:
            self.__bkg_fit = np.full(nb_sp, None)
        if len(self.__bkg_params.shape) != 2 \
                or self.__bkg_params.shape[1] != nb_sp:
            self.__bkg_params = np.full((2, nb_sp), float('nan'))

        self.__bkg_fit[index] = bkg_fit
        self.__bkg_params[index] = np.array(bkg_params).transpose(1, 0)
        return

    def remove_bkg_poly(self, inf, sup):
        if self.__data.shape[2] != self.__bkg_fit.shape[0]:
            self.__bkg_fit = np.full(self.__data.shape[2], None)
        if self.__data.shape[2] != self.__bkg_params.shape[0]:
            self.__bkg_params = np.full((4, 2, self.__data.shape[2]), None)
        for i in range(self.__data.shape[2]):
            inf_id, sup_id = map(int, self.get_index([inf, sup], spc=i)[:, 0])
            bkg_data = np.concatenate((
                self.__data[:inf_id+1, :, i],
                self.__data[sup_id:, :, i]
                ))

            def polyfit(x, a_0, a_1, a_2, a_3):
                return a_0 + a_1 * x + a_2 * x**2 + a_3 * x**3
            popt, pcov = sc.optimize.curve_fit(polyfit,
                                               bkg_data[:, 0],
                                               bkg_data[:, 1])
            perr = np.sqrt(np.diag(pcov))
            self.__bkg_fit[i] = lambda x, p: polyfit(x, p[0], p[1], p[2], p[3])
            bkg = self.__bkg_fit[i](self.__data[:, 0, i], popt)
            self.__data[:, 1, i] -= bkg
            self.__data[:, 2, i] += bkg
            self.__bkg_params[:, :, i] = np.concatenate(
                    np.atleast_2d(popt, perr)
                    ).transpose(1, 0)
        return

    def get_index(self, values, spc=0, col=0):
        arr = self.__data[:, col, spc]
        n = len(values)
        indices = np.concatenate(
                np.atleast_2d([0] * n, [arr[0] - v for v in values])
                ).transpose(1, 0)
        for i in range(1, arr.size):
            val = arr[i]
            for j in range(indices.shape[0]):
                diff = val - values[j]
                if abs(diff) < abs(indices[j, 1]):
                    indices[j] = i, diff
        return indices

    def fit_lbwf(self, p0=None, min_shift=None, max_shift=None):  # max exclude
        if min is not None and max is not None:
            min_id, max_id = map(
                    int,
                    self.get_index([min_shift, max_shift])[:, 0]
                    )
            max_id += 1
        else:
            if min is None:
                if max is None:
                    min_id, max_id = 0, self.__data.shape[0]
                else:
                    min_id = 0
                    max_id = int(self.get_index([max_shift])[0, 0])
            else:
                min_id = int(self.get_index([min_shift])[0, 0])
                max_id = self.data.shape[0]
        data_red = self.__data[min_id:max_id, :, :]

        def lorentz(w, w_max, I_max, fwhm):
            return I_max * (fwhm / 2)**2 / ((w - w_max)**2 + (fwhm / 2)**2)

        def bwf(w, w_max, I_max, fwhm, Q):
            return I_max * (1 + (2 * (w - w_max) / (Q * fwhm))**2) / \
                    (1 + (2 * (w - w_max) / fwhm)**2)

        def lbwf(w, w_bwf, I_bwf, fwhm_bwf, Q_bwf, w_l, I_l, fwhm_l, offset):
            return bwf(w, w_bwf, I_bwf, fwhm_bwf, Q_bwf) \
                    + lorentz(w, w_l, I_l, fwhm_l) \
                    + offset

        self.__fit = np.full(self.__data.shape[2], lbwf)
        self.__params = np.empty((8, 2, self.__data.shape[2]))

        for i in range(data_red.shape[2]):
            popt, pcov = sc.optimize.curve_fit(
                    lbwf,
                    data_red[:, 0, i],
                    data_red[:, 1, i],
                    p0=p0
                    )
            perr = np.sqrt(np.diag(pcov))
            self.__params[:, :, i] = np.concatenate(
                    np.atleast_2d(popt, perr)
                    ).transpose(1, 0)
        return

    def normalize(self):
        self.__class_width = (self.__data[-1, 0, :] - self.data[0, 0, :]) \
                / (self.__data.shape[0] + 1)

        self.__norm = np.linalg.norm(self.__data[:, 1, :], axis=0, ord=2) \
            * self.__class_width

        self.__data[:, 1, :] /= self.__norm
        self.__data[:, 2, :] /= self.__norm
        self.__bkg_params[:, 0] /= self.__norm
        self.__bkg_params[:, 1, :] = (self.__bkg_params[:, 1, :]
                                      / self.__norm)**2
        return

    # def normalize(self, norm_min=True, norm_max=True):
    #     if norm_max:
    #         max_val = self.__data[:, 1, :].max(axis=0)
    #         min_val = self.__data[:, 1, :].min(axis=0)
    #         factor = 1 / (max_val - min_val)
    #         if norm_min:
    #             offset = min_val
    #         else:
    #             offset = np.zeros_like(factor)
    #         self.__data[:, 1, :] = (self.__data[:, 1, :] - offset) * factor
    #         self.__data[:, 2, :] = (self.__data[:, 2, :] - offset) * factor
    #         self.__norm = np.concatenate(
    #                 np.atleast_2d(factor, offset)
    #                 ).transpose(1, 0)
    #         return
    #     msg = '"norm_max set to False is not yet implemented.'
    #     print('[' + '\033[1m\033[33m' + ' ERROR ' + '\033[0m' + ']> '
    #           + msg)
    #     raise NotImplementedError
