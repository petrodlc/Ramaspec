---
title: spectra.mean_fit
layout: page
parent: spectra
---

# `spectra.mean_fit`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

The mean fit from all spectrums.

One-dimensional table, storing mean fit line computed at call time from [`spectra.mean_fit_params`][mean_fit_params].
It needs [`spectra.mean_fit_params`][mean_fit_params] to be initialized.

Refer to [`spectra.fit`][fit] for for details on the fit function.

- *m* is the number of measure points par spectrum (should be the same for all)

### Getter

#### Returns
{: .no_toc }
- mean_count ([`numpy.ndarray`][ndarray]{:target="_blank"}(`numpy.float`) of shape (*m*, 2)):\
  a copy of the actual mean intensity stored in [`spectra.mean_data[:, 0, :]`][mean data]

<!--------------------------------------------------------------------------->

[fit]: {{ site.url }}/Documentation/Spectra/Properties/fit "spectra.fit"
[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[data setter]: {{ site.url }}/Documentation/Spectra/Properties/data#setter "spectra.data setter"
[mean data]: {{ site.url }}/Documentation/Spectra/Properties/mean_data "spectra.mean_data"
[compute mean data]: {{ site.url }}/Documentation/Spectra/Methods/compute_mean_data "spectra.compute_mean_data"
[ndarray]: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html "numpy.ndarray"
