import numpy as np
import matplotlib.pyplot as plt
# import pathlib as pth
import inspect
import scipy as sc


class spectrum:
    __name = ""
    __shift = np.empty(0)
    __count = np.empty(0)
    __bkg = np.empty(0)
    __bkg_fit = None
    __fit = None
    __bkg_params = np.empty(0)
    __params = np.empty(0)

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
    def shift(self):
        return self.__shift.copy()

    @property
    def count(self):
        return self.__count.copy()

    @property
    def bkg(self):
        return self.__bkg.copy()

    @property
    def data(self):
        return np.concatenate(
            (np.reshape(self.__shift, (self.__shift.shape[0], 1)),
             np.reshape(self.__count, (self.__count.shape[0], 1)),
             np.reshape(self.__bkg, (self.__bkg.shape[0], 1))),
            axis=1
            )

    @property
    def bkg_fit(self):
        return self.__bkg_fit

    @property
    def bkg_params(self):
        return self.__bkg_params.copy()

    @property
    def fit(self):
        return self.__fit

    @property
    def params(self):
        return self.__params.copy()

# #############################################################################

    @name.setter
    def name(self, name):
        self.__name = str(name)
        return self.name

    @shift.setter
    def shift(self, shift):
        shift_temp = np.array(shift, copy=True)
        if shift_temp.shape != self.__count.shape:
            msg = 'Array shapes do not match'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        if len(shift_temp.shape) != 1:
            msg = 'Array should be one dimensional'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        self.__shift = shift_temp
        return self.__shift

    @count.setter
    def count(self, count):
        count_temp = np.array(count, copy=True)
        if self.__shift.shape != count_temp.shape:
            msg = 'Array shapes do not match'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        if len(count_temp.shape) != 1:
            msg = 'Array should be one dimensional'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        self.__count = count_temp
        return self.__count

    @bkg.setter
    def bkg(self, bkg):
        bkg_temp = np.array(bkg, copy=True)
        if self.__shift.shape != bkg_temp.shape:
            msg = 'Array shapes do not match'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        if len(bkg_temp.shape) != 1:
            msg = 'Array should be one dimensional'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        self.__bkg = bkg_temp
        return self.__bkg

    @data.setter
    def data(self, data):
        shift_temp = np.array(data[:, 0], copy=True)
        count_temp = np.array(data[:, 1], copy=True)
        bkg_temp = np.array(data[:, 2], copy=True)
        if shift_temp.shape != count_temp.shape \
                or shift_temp.shape != bkg_temp.shape:
            msg = 'Array shapes do not match'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        if len(shift_temp.shape) != 1:
            msg = 'Arrays should be one dimensional'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        self.__shift = shift_temp
        self.__count = count_temp
        self.__bkg = bkg_temp
        return self.data

    @bkg_fit.setter
    def bkg_fit(self, bkg_fit):
        sig = inspect.signature(bkg_fit)
        if len(sig.parameters) != 2:
            msg = 'The fit function should take two arguments: ' \
                    'the variable and an array of parameters.'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        self.__bkg_fit = bkg_fit
        return self.__bkg_fit

    @bkg_params.setter
    def bkg_params(self, bkg_params):
        bkg_params_temp = np.array(bkg_params, copy=True)
        if len(bkg_params.shape) != 1:
            msg = 'Parameters array should be one dimensional'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        self.__bkg_params = bkg_params_temp
        return self.__bkg_params

    @fit.setter
    def fit(self, fit):
        sig = inspect.signature(fit)
        if len(sig.parameters) != 2:
            msg = 'The fit function should take two arguments: ' \
                    'the variable and an array of parameters.'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        self.__fit = fit
        return self.__fit

    @params.setter
    def params(self, params):
        params_temp = np.array(params, copy=True)
        if len(params.shape) != 1:
            msg = 'Parameters array should be one dimensional'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            raise ValueError
        self.__params = params_temp
        return self.__params

# #############################################################################

    @name.deleter
    def name(self):
        self.__name = ''
        return

# #############################################################################
# ################################# METHODS ###################################
# #############################################################################

    def read_from_file(self, path, mode='t', override_name=True):
        if mode == 'b':
            raise NotImplementedError
        if mode != 't':
            raise ValueError
        with open(path, 'rt', encoding='utf-8') as file:
            sep_data = list(map(float, file.read().split()))
        if override_name or self.__name == '':
            self.__name = ' '.join(path.stem.split("_"))
        self.__count = np.array(sep_data[1::2])
        self.__bkg = np.zeros_like(self.__count)
        if len(sep_data) % 2:
            self.__shift = np.array(sep_data[0:-1:2])
            msg = 'Uneven columns, excedent value has been skipped.'
            print('[' + '\033[1m\033[31m' + ' ERROR ' + '\033[0m' + ']> '
                  + msg)
            return self.data
        self.__shift = np.array(sep_data[0::2])
        return

    def remove_bkg_linear(self, low_center, top_center, low_range, top_range):
        low = []
        top = []
        for i in range(self.__shift.shape[0]):
            shift = self.__shift[i]
            if abs(shift - low_center) <= low_range * 0.5:
                low.append([shift, self.__count[i]])
            if abs(shift - top_center) <= top_range * 0.5:
                top.append([shift, self.__count[i]])
        low_anchor = np.array(low)
        top_anchor = np.array(top)
        low_anchor_mean = low_anchor.mean(axis=0)
        top_anchor_mean = top_anchor.mean(axis=0)

        slope = (top_anchor_mean[1] - low_anchor_mean[1]) / \
                (top_anchor_mean[0] - low_anchor_mean[0])
        height = low_anchor_mean[1] - slope * low_anchor_mean[0]
        self.__bkg_fit = lambda x, p: p[0] * x + p[1]
        self.__bkg_params = np.array([slope, height])
        self.__bkg = self.__bkg_fit(self.__shift, self.__bkg_params)
        self.__count -= self.__bkg
        return

    def fit_lbwf(self, p0=None, save=True):
        def lorentz(w, w_max, I_max, fwhm):
            return I_max * (fwhm / 2)**2 / ((w - w_max)**2 + (fwhm / 2)**2)

        def bwf(w, w_max, I_max, fwhm, Q):
            return I_max * (1 + (2 * (w - w_max) / (Q * fwhm))**2) / \
                    (1 + (2 * (w - w_max) / fwhm)**2)

        def lbwf(w, w_bwf, I_bwf, fwhm_bwf, Q_bwf, w_l, I_l, fwhm_l):
            return lorentz(w, w_l, I_l, fwhm_l) \
                    + bwf(w, w_bwf, I_bwf, fwhm_bwf, Q_bwf)

        if p0 is None:
            popt, pcov = sc.optimize.curve_fit(
                    lbwf,
                    self.__shift,
                    self.__count
                    )
        else:
            popt, pcov = sc.optimize.curve_fit(
                    lbwf,
                    self.__shift,
                    self.__count,
                    p0=p0
                    )

        perr = np.sqrt(np.diag(pcov))

        p_fit = np.concatenate(
                (
                    popt.reshape((popt.shape + (1,))),
                    perr.reshape((perr.shape + (1,)))
                    ),
                axis=1
                )

        if save:
            self.__fit = lambda x, p: lbwf(x,
                                           p[0],
                                           p[1],
                                           p[2],
                                           p[3],
                                           p[4],
                                           p[5],
                                           p[6])
            self.__params = p_fit
        return

    def plot(self, to_plot=[True, False, False, False], ret=False):
        if not np.any(to_plot):
            return

        _, ax = plt.subplots()

        if to_plot[0]:
            ax.plot(self.__shift, self.__count)
        if to_plot[1]:
            ax.plot(self.__shift, self.__count + self.__bkg)
        if to_plot[2]:
            ax.plot(self.__shift, self.__bkg)
        if to_plot[3]:
            ax.plot(self.__shift,
                    self.__fit(self.__shift, self.__params[:, 0]))
        ax.set_title(self.__name)
        plt.show()
        if ret:
            return ax
        return


class spectra:
    __name = ''
    __data = np.full(0, None)
    __mean_data = np.full(0, None)
    __bkg_fit = None
    __bkg_params = np.full(0, None)
    __fit = None
    __params = np.full(0, None)
    __mean_params = np.full(0, None)
    __shift_offset = np.zeros(0)
    __norm = np.zeros(0)

    def __init__(self):
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

    @mean_data.deleter
    def mean_data(self):
        self.__mean = spectrum()
        return

# #############################################################################
# ################################# METHODS ###################################
# #############################################################################

    def set_spectrums(self, spectrums):
        self.__data = np.array([s.data for s in spectrums]).transpose(1, 2, 0)
        self.__shift_offset = np.zeros(self.__data.shape[0])
        return

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
        for file in files:
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
            self.__fit[i] = lambda x, p: polyfit(x, p[0], p[1], p[2], p[3])
            bkg = self.__fit[i](self.__data[:, 0, i], popt)
            self.__data[:, 1, i] -= bkg
            self.__data[:, 2, i] += bkg
            self.__bkg_params = np.concatenate(
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

    def shift_axis(self, offset, spc=None):
        if spc is None:
            self.__data[:, 0, :] += offset
            self.__shift_offset += offset
            return
        self.__data[:, 0, spc] += offset
        self.__shift_offset[spc] += offset
        return

    def normalize(self, norm_min=True, norm_max=True):
        if norm_max:
            max_val = self.__data[:, 1, :].max(axis=0)
            min_val = self.__data[:, 1, :].min(axis=0)
            factor = 1 / (max_val - min_val)
            if norm_min:
                offset = min_val
            else:
                offset = np.zeros_like(factor)
            self.__data[:, 1, :] = (self.__data[:, 1, :] - offset) * factor
            self.__data[:, 2, :] = (self.__data[:, 2, :] - offset) * factor
            self.__norm = np.concatenate(
                    np.atleast_2d(factor, offset)
                    ).transpose(1, 0)
            return
        msg = '"norm_max set to False is not yet implemented.'
        print('[' + '\033[1m\033[33m' + ' ERROR ' + '\033[0m' + ']> '
              + msg)
        raise NotImplementedError
