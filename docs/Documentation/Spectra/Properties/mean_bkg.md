---
title: spectra.mean_bkg
layout: page
parent: spectra
---

# `spectra.mean_bkg`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

The mean background from all spectrums.

Two-dimensional table, storing background intensity mean values (`spectra.mean_count[:, 0]`) and standard deviation (`spectra.mean_count[:, 1]`)
computed along 3<sup>rd</sup> axis (spectrums) of [`spectra.data`][data].
Its value is distinct from the default only after [`spectra.compute_mean_data`][compute mean data] has been called
and before [`spectra.data`][data] is [set][data setter] to a new value.

This is equivalent to [`spectra.mean_data[:, 2, :]`][mean data]

- *m* is the number of measure points par spectrum (should be the same for all)

### Getter

#### Returns
{: .no_toc }
- mean_bkg ([`numpy.ndarray`][ndarray]{:target="_blank"}(`numpy.float`) of shape (*m*, 2)):\
  a copy of the actual mean background intensity stored in [`spectra.mean_data[:, 2, :]`][mean data]

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[data setter]: {{ site.url }}/Documentation/Spectra/Properties/data#setter "spectra.data setter"
[mean data]: {{ site.url }}/Documentation/Spectra/Properties/mean_data "spectra.mean_data"
[compute mean data]: {{ site.url }}/Documentation/Spectra/Methods/compute_mean_data "spectra.compute_mean_data"
[ndarray]: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html "numpy.ndarray"
