---
title: log.styles
layout: page
parent: log
---

# `log.styles`
{: .no_toc }

<details close markdown="block">
  <summary>
    Table of Contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

List all available styles (based on [ANSI escape codde][escape code]{:target="_blank"}).

{: .note-title }
> See also
>
> [`log.print_styles`][print_styles]: print style examples

### Getter

#### Returns
{: .no_toc }
- `str`

### Setter

#### Parameters
{: .no_toc }
- name (`str` or anything that can be converted to `str`)

### Deleter

Resets the name to an empty `str` (`''`).

<!--------------------------------------------------------------------------->

[print_styles]: {{ site.url }}/Documentation/Log/methods/print_styles "log.print_styles"
[escape code]: https://en.wikipedia.org/wiki/ANSI_escape_code "ANSI escape code (Wikipedia)"
