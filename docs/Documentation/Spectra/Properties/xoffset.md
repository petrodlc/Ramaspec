---
title: spectra.xoffset
layout: page
parent: spectra
---

# `spectra.xoffset`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

The raman shift correction for each spectrum.

One-dimensional table, storing the offset added to [raman shift][data] for each spectrum, after [`spectra.shift_x`][shift_x] has been called.

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
[shift_x]: {{ site.url }}/Documentation/Spectra/Methods/shift_x "spectra.shift_x"
[ndarray]: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html "numpy.ndarray"
