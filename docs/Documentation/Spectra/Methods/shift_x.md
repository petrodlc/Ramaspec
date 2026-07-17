---
title: spectra.shift_x
layout: page
parent: spectra
---

# `spectra.shift_x`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

```python
spectra.shift_x(xoffset)
```

Adds an offset to raman shift for each spectrum.

Shift [`spectra.data[:, 0, :]`][data] with the offset provided.
Offset can be ifferent for each spectrum.

### Parameters

- xoffset: `float` or *Array-like* of `float`\
  If it is a `float` or an *array-like* with a length different than *n*, all spectrum will be shifted by the same amount (`xoffset[0]` in case of an array).
  If an array is provided whose size matches the number of spectrum in the `spectra` instance, each of the lasts coul be shifte by a different amount.

### Returns

No return value

### Notes

{: .warning }
No check is performed to ensure that *xoffset* is one-dimensionnal.

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
