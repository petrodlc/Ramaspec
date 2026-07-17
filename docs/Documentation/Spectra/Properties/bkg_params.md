---
title: spectra.bkg_params
layout: page
parent: spectra
---

# `spectra.bkg_params`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

The parameters of the fitted baseline.

Three-dimensional table, storing background fit parameters and associated uncertainties for each spectrum, computed when [`spectra.remove_bkg_poly`][remove_bkg_poly] is called.

- *n* represents the number of spectrums in this class instance
- *ord* is the order of the polynomial used to fit the baseline + 1

### Getter

#### Returns
{: .no_toc }
- bkg_params ([`numpy.ndarray`][ndarray]{:target="_blank"}(`numpy.float`) of shape (*ord*, 2, *n*)):\
  a copy of the actual background parameters stored in the class

### Deleter

Resets to a [`numpy.ndarray`][ndarray]{:target="_blank"} of size (0, 2, *n*) filled with `None`, where *n* is computed from current shape of [`spectra.data`][data]

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[remove_bkg_poly]: {{ site.url }}/Documentation/Spectra/Methods/remove_bkg_poly "spectra.remove_bkg_poly"
[ndarray]: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html "numpy.ndarray"
