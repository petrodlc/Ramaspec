---
title: spectra.mean_fit_params
layout: page
parent: spectra
---

# `spectra.mean_fit_params`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

The mean raman peaks parameters from all spectrums.

Two-dimensional table, storing fit parameters mean values (`spectra.mean_fit_params[:, 0]`), propagated errors (`spectra.mean_fit_params[:, 1]`) and standard deviations (`spectra.mean_fit_params[:, 2]`) computed along 3<sup>rd</sup> axis (spectrums) of [`spectra.fit_params`][fit_params].
Its value is distinct from the default only after [`spectra.compute_mean_fit_params`][compute_mean_fit_params] has been called
and before [`spectra.data`][data] is [set][data setter] to a new value.

### Getter

#### Returns
{: .no_toc }
- mean_fit_params ([`numpy.ndarray`][ndarray]{:target="_blank"}(`numpy.float`) of shape (8, 3)):\
  a copy of the actual mean fit parameters stored

### Deleter

Resets to a [`numpy.ndarray`][ndarray]{:target="_blank"} of size (8, 3) filled with `None`

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[data setter]: {{ site.url }}/Documentation/Spectra/Properties/data#setter "spectra.data setter"
[fit_params]: {{ site.url }}/Documentation/Spectra/Properties/fit_params "spectra.fit_params"
[compute_mean_fit_params]: {{ site.url }}/Documentation/Spectra/Methods/compute_mean_fit_params "spectra.compute_mean_fit_params"
[ndarray]: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html "numpy.ndarray"
