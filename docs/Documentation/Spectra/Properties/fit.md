---
title: spectra.fit
layout: page
parent: spectra
math: mathjax
---

# `spectra.fit`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

The fits for each spectrums.

Two-dimensional table, storing fitted line for each spectrum, computed at call time from [`spectra.fit_params`][fit params].

The fit is the sum of a Cauchy (or Lorentz) distribution (for D peak) and a Breit-Wigner-Fano (BWF) distribution (for G peak), with a parameter controlling the vertical offset added:

$$
f_{LBWF}(w, p) = I_D \frac{\left(\frac{\Gamma_D}{2}\right)^2}{\left(w - w_D\right)^2 + \left(\frac{\Gamma_D}{2}\right)^2}
               + I_G \frac{\left(1 + \left(2\cdot\frac{w - w_G}{Q\Gamma_G}\right)\right)^2}{1 + \left(2\cdot\frac{w - w_G}{\Gamma_G}\right)^2}
               + y_0
$$

with $$ p = \left[w_G, I_G, \Gamma_G, \frac{1}{Q}, w_D, I_D, \Gamma_D, y_0\right] $$
and parameters represent:

|$$ w_G $$, $$ w_D $$          | the position of G and D peak respectively (if $$ \frac{1}{Q} \ll 1 $$, and $$ \left\|w_G - w_D\right\| $$ is large enough that the two peaks are clearly distinct)|
|$$ I_G $$, $$ I_D $$          | the maximum intensity of the peaks (at $$ w_G $$ and $$ w_D $$)|
|$$ \Gamma_G $$, $$ \Gamma_D $$| the full with at half maximum (FWHM) of each peak|
|$$ \frac{1}{Q} $$             | the asymmetric factor of G peak|
|$$ y_0 $$                     | the vertical offset added to let the function reach $$ 0 $$|

- *n* represents the number of spectrums in this class instance
- *m* is the number of measure points par spectrum (should be the same for all)

### Getter

#### Returns
{: .no_toc }
- fit ([`numpy.ndarray`][ndarray]{:target="_blank"}(`numpy.float`) of shape (*m*, *n*)):\
  the computted fit lines

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[fit params]: {{ site.url }}/Documentation/Spectra/Properties/fit_params "spectra.fit_params"
[ndarray]: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html "numpy.ndarray"
