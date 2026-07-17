---
title: Usage
layout: page
nav_order: 2
---
# Usage
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

Since {{ site.title }} consists mainly on several files containing one class, all that is needed is to import these files.

## Import
If your working directory is `/path/to/my/project`, and {{ site.title }} is installed in `/path/to/my/project/{{ site.title }}`:
```python
import {{ site.title }}.spectra as sp
```
and if you want logging utility outside of [`spectra`][spectra] class:
```python
import {{ site.title }}.log
```

## Plot

No plotting utility is currently added as matplotlib.pyplot works fine as is. If you want ploting capabilities, import this library as well :
```python
import matplotlib.pyplot as plt
```
For matplotlib usage, chack its [documentation](https://matplotlib.org/stable/api/index.html).

## Workflow
{{ site.title }} is designed with live processing from python console in mind: main class and several custom scrits for automated basic actions, such as preprocessing are imported, then the main processing occurs in console.

### Basic workflow
{: .no_toc }
1. In python files, write scripts and function to handle processing steps that are often repeated, such as preprocessing.
2. Compute and store variables for simpler use in processing, like path to data.
3. Import every thing and `{{ site.title }}.spectra` file from within python console
4. Ready to process data !

{: .important }
> All processes repeated that do not need any human action could and **shoud** be written to python files.
> The purpose of live processing is not to make the same things again and again, but to be able to adapt processing depending of what data look like.
>
> Once the whole prcessing steps are clearly defined, and all that is left is to process the whole dataset blindly with this parameters, juste write a script, and call it once.

<!--------------------------------------------------------------------------->

[spectra]: {{ site.url }}/Documentation/Spectra/ "spectra"
