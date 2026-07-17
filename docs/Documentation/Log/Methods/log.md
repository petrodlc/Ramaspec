---
title: log.log
layout: page
parent: log
---

# `log.log`
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
spectra.log(msg, keyword, style, keyword_style, log_level=2)
```

Base method of all the class.

### Parameters

- msg: `str`\
  The message to add to logs.
- keyword: `str`\
  A word (preferably 9 letters or less) to qualify the type of the message.
- style: `list` of `str`\
  The style to use for all but the message and the keyword, taken from [`log.styles`][styles].
- keyword_style: `list` of `str`\
  The style of the keyword, taken from [`log.styles`][styles].
- log_level: `int`\
  Select by importance which messages are printed and which are only stored silently.
  The lower it is, the more restricive it gets.
  `-1` is the only allowed negative number, and stands for "quiet mode" (no message printed).

### Returns

No return value

<!--------------------------------------------------------------------------->

[styles]: {{ site.url }}/Documentation/Log/Properties/styles "log.styles"
