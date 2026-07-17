---
title: spectra.data
layout: page
parent: spectra
---

# `spectra.data`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

The main data contained in the class.
Three-dimensional table, storing raman shifts and corresponding signal and background intensities for each spectrum.
Background intensity is the part substracted from the signal after baseline has been fitted with [`spectra.remove_bkg_poly`][remove_bkg_poly].

- *n* represents the number of spectrums in this class instance
- *m* is the number of measure points par spectrum (should be the same for all)
- \* is any size

### Getter

#### Returns
{: .no_toc }
- data ([`numpy.ndarray`][ndarray]{:target="_blank"}(`numpy.float`) of shape (*m*, 3, *n*)):\
  a copy of the actual data stored in the class

### Setter

Raplace the old data with a copy of the data provided, and resets all other attributes except [`name`][name] to their default value.

#### Parameters
{: .no_toc }
- data (array like (`float`) of shape (*, 3, *)):\
  the data to store

### Deleter

Resets to a [`numpy.ndarray`][ndarray]{:target="_blank"} of size (0, 3, 0) filled with `None`.
Resets all properties but [`name`][name] to their default values.

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[name]: {{ site.url }}/Documentation/Spectra/Properties/name "spectra.name"
[remove_bkg_poly]: {{ site.url }}/Documentation/Spectra/Methods/remove_bkg_poly "spectra.remove_bkg_poly"
[ndarray]: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html "numpy.ndarray"
