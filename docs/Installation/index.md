---
title: Installation
layout: page
nav_order: 1
---

# Installation
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

Here comes installation instructions.

## Dependencies

### For python only

#### Dependencies required:
{: .no_toc}
- [python](https://www.python.org/downloads/) (tested only with python 3.14.5)
- [numpy](https://numpy.org/install/)  (tested with v2.4.6)
- [scipy](https://scipy.org/install/) (tested with v1.17.1)
- pathlib (should be installed along with python)

{: .note }
Python libraries should be installed in a [virtual environment](https://docs.python.org/3/library/venv.html).

#### Recommended:
{: .no_toc }
- [git](https://git-scm.com/install/windows) (for installation and updates, tought it is still possible to download raw files without it)
- [matplotlib](https://matplotlib.org/stable/install/index.html), as no plotting utility is provided

### For documentation
- [Jekyll](https://jekyllrb.com/docs/installation/), see its own dependencies (can be installed throught [Bundler](https://bundler.io/))

## Install

Navigate to any place on your computer where you want it installed, and clone the git repository:
```sh
git clone https://github.com/petrodlc/Ramaspec.git
```

## Update
From within the installation directory, run the following git command:
```bash
git pull
```
