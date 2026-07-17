---
title: spectra.fit_lbwf
layout: page
parent: spectra
---

# `spectra.fit_lbwf`
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
spectra.fit_lbwf(p0=numpy.ones(8), fit_range=None)
```

Make a LBWF fit of the signal.

Tries to ajust a Lorentz (or Cauchy) and a Breit-Wigner-Fano distribution on the signal stored in [`spectra.data`][data].

For more details on the fit, refer to [`spectra.fit`][fit].

### Parameters

- p0: *Array-like* of shape (8)\
  The initial values of the fit parameters (see [`scipy/optimize.curve_fit`][curve_fit]{:traget="_blank"})
- fit_range: *Array-like* of shape (2)\
  The spectral range on which to fit the signal.

### Returns

No return value

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[fit]: {{ site.url }}/Documentation/Spectra/Properties/fit "spectra.fit"
[curve_fit]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html "scipy.optimize.curve_fit"
