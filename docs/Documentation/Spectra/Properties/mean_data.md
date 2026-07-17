---
title: spectra.mean_data
layout: page
parent: spectra
---

# `spectra.mean_data`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

The mean data from all spectrums.

Three-dimensional table, storing data mean values (`spectra.mean_data[:, :, 0]`) and standard deviation (`spectra.mean_data[:, :, 1]`) computed along 3<sup>rd</sup> axis (spectrums).
Its value is distinct from the default only after [`spectra.compute_mean_data`][compute mean data] has been called
and before [`spectra.data`][data] is [set][data setter] to a new value.

- *n* represents the number of spectrums in this class instance
- *m* is the number of measure points par spectrum (should be the same for all)

### Getter

#### Returns
{: .no_toc }
- mean_data ([`numpy.ndarray`][ndarray]{:target="_blank"}(`numpy.float`) of shape (*m*, 3, 2)):\
  a copy of the actual mean_data stored in the class instance

### Deleter

Defaults to a [`numpy.ndarray`][ndarray]{:target="_blank"} of shape (*m*, 3, 2) filled with `None`,
where *m* is computed from current shape of [`spectra.data`][data].

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[data setter]: {{ site.url }}/Documentation/Spectra/Properties/data#setter "spectra.data setter"
[compute mean data]: {{ site.url }}/Documentation/Spectra/Methods/compute_mean_data "spectra.compute_mean_data"
[ndarray]: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html "numpy.ndarray"
