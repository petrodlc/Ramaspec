---
title: spectra.set_range
layout: page
parent: spectra
---

# `spectra.set_range`
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
spectra.set_range(inf, sup)
```

Sets the spectral winddow.

Removes every data but the ones with raman shift in the specified range.
[`spectra.mean_ata`][mean_data] is affected too.

### Parameters

- inf, sup: `floats`\
  Inferior an superior boundaries of the spectral window.
  They correspond to the raman shifts, not the table indices.

### Returns

No return value

### Notes

{: .warning }
> If `inf` is equal to `sup`, the function returns without affecting data.
>
> To supress [`spectra.data`][data], use the `del` keyworld.

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[mean_data]: {{ site.url }}/Documentation/Spectra/Properties/mean_data "spectra.mean_data"
