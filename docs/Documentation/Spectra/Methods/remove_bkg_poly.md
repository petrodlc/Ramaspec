---
title: spectra.remove_bkg_poly
layout: page
parent: spectra
math: mathjax
---

# `spectra.remove_bkg_poly`
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
spectra.remove_bkg_poly(inf, sup, ord=3, p0=None)
```

Remove background from signal.

Fit a polynomial on the signal, and substract it from the signal intensity.
The fitted signal is taken on the interval
$$ I \setminus \left] inf, sup \right[ $$
where $$ I $$ is the total spectral range.
Update [`spectra.data`][data] in consequence, if computation succeed.

The polynomial could be of any order greater or equal to zero.

### Parameters

- inf, sup: `floats`\
  The boundaries of the spectral range to ignore.
- ord: `int` $$ \ge 0 $$\
  The degree of the polynomial.
  Overrided if `p0` is not `None`.
  Shorthand for `p0=[1]*ord`
- p0: `None` or *Array-like* of `floats`\
  If not `None`, defines the initial parameters for the fit parameters.
  Refers to [`scipy.optimize.curve_fit` documentation][curve_fit]{:target="_blank"} for more information.

### Returns

No return value

### Note
{: .warning }
> Providing a negative value for `ord` can throw exceptions or cause unexpected behaviour.

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[curve_fit]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html "scipy.optimize.curve_fit"
