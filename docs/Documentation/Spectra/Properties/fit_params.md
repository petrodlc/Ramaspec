---
title: spectra.fit_params
layout: page
parent: spectra
---

# `spectra.fit_params`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

The parameters of the fitted signal.

Three-dimensional table, storing raman peaks fit parameters and associated uncertainties for each spectrum, computed when [`spectra.fit_lbwf`][fit_lbwf] is called.

To get computation detail on this fit, refer to [`spectra.fit`][fit] documentation.

- *n* represents the number of spectrums in this class instance

### Getter

#### Returns
{: .no_toc }
- bkg_params ([`numpy.ndarray`][ndarray]{:target="_blank"}(`numpy.float`) of shape (8, 2, *n*)):\
  a copy of the actual fit parameters stored in the class

### Deleter

Resets to a [`numpy.ndarray`][ndarray]{:target="_blank"} of size (8, 2, *n*) filled with `None`, where *n* is computed from current shape of [`spectra.data`][data]

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[fit]: {{ site.url }}/Documentation/Spectra/Properties/fit "spectra.fit"
[fit_lbwf]: {{ site.url }}/Documentation/Spectra/Methods/fit_lbwf "spectra.fit_lbwf"
[ndarray]: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html "numpy.ndarray"
