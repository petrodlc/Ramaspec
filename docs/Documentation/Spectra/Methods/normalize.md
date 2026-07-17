---
title: spectra.normalize
layout: page
parent: spectra
math: mathjax
---

# `spectra.normalize`
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
spectra.normalize()
```

Normalize signal and background for each spectrum.

Compute the norm of the signal function, then divide signal an backgroun intensities store in [`spectra.data`][data].
The norm used is


$$
\left\|f\right\|^2 = \int_I f\left(x\right)^2 dx
$$

where $$ f $$ is the function to normalize, and $$ I $$ is the interval of normalization.

For discrete cases, it become

$$
\left\|x\right\|^2 = \sum_i \Delta_i \cdot x_i^2
$$

with $$ x = \left[ x_0, x_1, \dots, x_n \right] $$ and $$ \left\{x_i\right\} \in f\left(I\right) $$.

$$ \left\{ \Delta_i \right\} $$ are the spaces between each values. If it is assume constant:

$$
\left\|x\right\|^2 = \Delta \sum_i x_i^2
$$

This method updates also the values andd uncertainties of [`spectra.bkg_params`][bkg_params]

### Parameters

No parameters

### Returns

No return value

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[bkg_params]: {{ site.url }}/Documentation/Spectra/Properties/bkg_params "spectra.bkg_params"
