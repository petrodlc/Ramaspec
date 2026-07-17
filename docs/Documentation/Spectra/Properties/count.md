---
title: spectra.count
layout: page
parent: spectra
---

# `spectra.count`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

The signal intensity for all spectrums.

Two-dimensional table, storing signal intensity for each spectrum, equivalent to [`spectra.data[:, 1, :]`][data].

- *n* represents the number of spectrums in this class instance
- *m* is the number of measure points par spectrum (should be the same for all)

### Getter

#### Returns
{: .no_toc }
- count ([`numpy.ndarray`][ndarray]{:target="_blank"}(`numpy.float`) of shape (*m*, *n*)):\
  a copy of the actual signal intensity stored in the [`data`][data] property

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[ndarray]: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html "numpy.ndarray"
