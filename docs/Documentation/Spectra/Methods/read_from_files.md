---
title: spectra.read_from_files
layout: page
parent: spectra
---

# `spectra.read_from_files`
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
spectra.read_from_files(files, mode='t', rename=None)
```

Read [`spectra.data`][data] from files.

Fill [`spectra.data`][data] with values read from a list of files.
Files should be space-separate values, without column header.

With files containing three columns, they are assume to be in the order: raman shift, signal, then backgroun intensity.
When less columns are present, the missing fields are filled with zeros.
Exceding columns are ignored, and empty files are skipped.

No check is ensured on files properties, so there coul be issues with very large files, or other common concern about file reading.

### Parameters

- files: *Array-like* of `str` or [`pathlib.Path`][path]{:target="_blank"}\
  Files from which [`spectra.data`][data] will be read, each file being one spectrum.
  All files should have the same number of lines.
- mode: *t* or *b*\
  The mode use to read files (see [python doc][read]{:target="_blank"}).
  Currently, only text mode (*t*) is supported.
- rename: `None` or `str`\
  If not `None`, set [`spectra.name`][name] to the string provided.
  If it is neither `None` nor a `str` object, tries to cast it to `str`.

### Returns

No return value

### Raises

| Exception | Cause|
| :-------- | :--- |
| `NotImplementedError` | If *b* is provided for file read mode |
| `ValueError` | If *mode* is neither *t* nor *b* |

<!--------------------------------------------------------------------------->

[data]: {{ site.url }}/Documentation/Spectra/Properties/data "spectra.data"
[name]: {{ site.url }}/Documentation/Spectra/Properties/name "spectra.name"
[path]: https://docs.python.org/3/library/pathlib.html#concrete-paths "pathlib.Path"
[read]: https://docs.python.org/3/tutorial/inputoutput.html#methods-of-file-objects "python input and output"
