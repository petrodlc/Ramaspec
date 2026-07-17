---
title: spectra.norm
layout: page
parent: spectra
---

# `spectra.norm`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

The normalization factor for each spectrum.

One-dimensional table, storing the factor multiplied with [raman shift][data] to normalize each spectrum, after [`spectra.normalize`][normalize] has been called.

It is resets after [`spectra.data`][data] is [set][data setter] to a new value.

- *n* represents the number of spectrums in this class instance

### Getter

#### Returns
{: .no_toc }
- xoffset ([`numpy.ndarray`][ndarray]{:target="_blank"}(`numpy.float`) of shape (*n*)):\
  a copy of the actual corrections stored

### Deleter

Resets to a [`numpy.ndarray`][ndarray]{:target="_blank"} of size (*n*) filled with `None`, where *n* is computed from current shape of [`spectra.data`][data]
  
<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[data setter]: {{ site.url }}/Documentation/Spectra/Properties/data#Setter "spectra.data setter"
[normalize]: {{ site.url }}/Documentation/Spectra/Methods/normalize "spectra.normalize"
[ndarray]: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html "numpy.ndarray"
