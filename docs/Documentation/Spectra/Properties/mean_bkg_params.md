---
title: spectra.mean_bkg_params
layout: page
parent: spectra
---

# `spectra.mean_bkg_params`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

The mean background parameters from all spectrums.

Two-dimensional table, storing background parameters mean values (`spectra.mean_bkg_params[:, 0]`), propagated errors (`spectra.mean_bkg_params[:, 1]`) and standard deviations (`spectra.mean_bkg_params[:, 2]`) computed along 3<sup>rd</sup> axis (spectrums) of [`spectra.bkg_params`][bkg_params].
Its value is distinct from the default only after [`spectra.compute_mean_bkg_params`][compute_mean_bkg_params] has been called
and before [`spectra.data`][data] is [set][data setter] to a new value.

- *ord* is the order of the polynomial used to fit the baseline + 1

### Getter

#### Returns
{: .no_toc }
- mean_bkg_params ([`numpy.ndarray`][ndarray]{:target="_blank"}(`numpy.float`) of shape (*ord*, 3)):\
  a copy of the actual mean background parameters stored

### Deleter

Resets to a [`numpy.ndarray`][ndarray]{:target="_blank"} of size (0, 3) filled with `None`

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[data setter]: {{ site.url }}/Documentation/Spectra/Properties/data#setter "spectra.data setter"
[bkg_params]: {{ site.url }}/Documentation/Spectra/Properties/bkg_params "spectra.bkg_params"
[compute_mean_bkg_params]: {{ site.url }}/Documentation/Spectra/Methods/compute_mean_bkg_params "spectra.compute_mean_bkg_params"
[ndarray]: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html "numpy.ndarray"
