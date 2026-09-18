<!-- -->
            +-------------------------------------------+
            +                                           +
            +                mathastext                 +
            +                                           +
            +     'Use the text font in math mode'      +
            +                                           +
            +-------------------------------------------+

This Work may be distributed and/or modified under the conditions
of the [LPPL 1.3c](https://www.latex-project.org/lppl/lppl-1-3c.txt)

The Author of this Work is Jean-Francois Burnol (`jfbu at free dot fr`)

Copyright (C) 2011-2019, 2022-2024 Jean-Francois Burnol

      Source: mathastext.dtx 1.4e 2024/10/26


DESCRIPTION
===========

Optimal typographical results for documents containing
mathematical symbols can only be hoped for with math fonts
specifically designed to match a given text typeface.
Although the list of freely available math fonts (alongside
the Computer Modern and AMS extension fonts) is slowly
expanding (fourier, kpfonts, mathdesign, pxfonts, txfonts,
newpx, newtx, ...) it remains limited, and the situation is
even worse with Unicode fonts (XeTeX/LuaTeX). So if you can't
find a math font which fits well with your favorite text
font, and wish to still be able to typeset mathematical
documents, perhaps not of the highest typographical quality,
but at least not subjected to obvious visual incompatibilities
between your text font and the math fonts, try out mathastext:
it will simply use the text font also for the math!

- http://jf.burnol.free.fr/mathastext.html
- http://jf.burnol.free.fr/showcase.html

USAGE
=====

`mathastext` is a LaTeX package

      \usepackage{mathastext}

The document will use in math mode the text font as configured at
package loading time, for these characters:

      abcdefghijklmnopqrstuvwxyz
      ABCDEFGHIJKLMNOPQRSTUVWXYZ
      0123456789
      !?,.:;+-=()[]/#$%&<>|{}\

Main options: `italic`, `frenchmath`, `subdued`, `LGRgreek`.
- Use the `italic` option to get the Latin letters in math mode
  be in italics. Digits and log-like operator names (pre-defined
  as well as user-defined) will be in the same shape as the text
  font (usually this means upright).
- each `\Mathastext[<name>]` in the preamble defines a math version
  to be later activated in the document body via the command
  `\MTversion{<name>}`.
- With the `subdued` option, mathastext will be active
  only inside such math versions.
- For documents needing Greek letters the following is
  possible:
  - no option: Greek letters defined by other packages,
  - `eulergreek`: use the Euler font for the Greek letters,
  - `symbolgreek`: use the Postscript Symbol font for the
     Greek letters.
  - `LGRgreek`: use the document text font in LGR encoding.
     Further options specify the shape of the lowercase
     and uppercase Greek glyphs; starting with v1.15c it is
     possible to use multiple distinct LGR fonts in the
     same document.
- Commands are provided to scale the Euler and Symbol fonts by an
  arbitrary factor to let them fit better with the document text
  font.
- `\MTsetmathskips` allows to set up extra spacings around letters.

RECENT CHANGES
==============

1.4e \[2024/10/26\]
----

* Fix a bug dating back to `1.3y` which caused under `LGRgreek` or
  `LGRgreeks` options an `\MTversion{normal}` to raise an `Extra
  \else` error (not if `subdued`).  The unit test which could have
  shown this had been left aside at `1.4d` because it was so old
  that some matters unrelated to the package prevented its
  immediate use... alas...

* Fix one more `1.4` regression: the (not really recommended)
  option `unimathaccents` was broken.  Again a test file existed
  but it had been left apart from those automatically built, for
  some unknown reason...

1.4d \[2024/10/26\]
----

* Fix one more `1.4` regression (the worst one by far): `$f''$`
  caused a crash.  Fortunately, the `everymath` option which
  re-enacts legacy code could be used as a *temporary emergency
  work-around*.  Thanks to Enrico Gregorio for report.

* The `1.4b` option `noletters` did not prevent the package from
  defining math mode symbols `\inodot` and `\jnodot`.  It now does.

* Fix a longstanding legacy bug which would have caused a crash if
  `\MTnonlettersobeymathxx` had been used with `XeLaTeX` in a
  document with the character `-` being a Babel shorthand.

* Usage of `\Mathastext` or `\MTDeclareVersion` to declare a
  math version associated with an exotic non-text font encoding
  such as `OML` is theoretically possible (although of dubious
  practical use except for stress tests) but was broken
  since `1.3u` due to internals
  relying on `LaTeX` commands associated with text font encodings
  (for example to define `\inodot`
  using `\i`,
  or the `\hbar` with the help of the accent command `\=`)
  and which are not available in such context.  This release
  handles such situation gracefully via warnings, rather than
  causing low level errors.

* Improve looks in the PDF of this Change log.

1.4c \[2024/10/21\]
----

* Fix a regression at `1.4`: under `XeLaTeX`, loading `mathastext`
  caused an error if `unicode-math` and its `\setmathfont` had been
  used prior ("*Extended mathchar used as mathchar*" in relation to the
  minus sign character). Thanks to Michael Roland for report.

  Keep in mind though that the documentation (see 1.4.15 Unicode engines) has
  always said that the package "*is expected to be most definitely
  incompatible with unicode-math*".

* Fix another regression at `1.4`, related to the same code and also avoided
  with `everymath` option, but showing with
  all engines.  It caused `\MTnonlettersdonotobeymathxx`, if used, to reset
  the minus sign to its status as prior to the loading of `mathastext`,
  whereas it should have used the (by default) mathversion dependent one
  (which defaults to the en-dash in the font encoding as stored by `mathastext` in
  the extended math version).

* `\Relbar` and `\relbar` redeclarations (needed as they are used by `LaTeX`
  for arrows, and the equal and minus signs if picked from the text font may not
  work well in-there) are now done via `\DeclareRobustCommand` also with
  package `amsmath` to match the current behavior of the latter.  Note though
  that they will use the equal and minus signs as in place at package loading
  time, the documentation does say that `mathastext` should be loaded last.

1.4b \[2024/07/27\]
----

* Fix a regression at `1.4` regarding option `nodigits`.

* New option: `noletters`.  *I am in old age now so I can provide an option
  completely antithetical to my life work*.

* Option `everymath` which is destined to be removed at next major
  release warns user about it.  As major releases tend to happen once
  per decade I think the constant nagging will become insufferable
  and you will adapt to the `1.4` changes rather than persisting into
  using this option.

1.4a \[2024/07/20\]
----

* There was a documentation glitch in 1.4 and also a problem with the
  `\MTprimeskip` feature being lost under the emergency fall-back
  `everymath` option.

1.4 \[2024/07/20\]
---

* Since 1.2 of 2012/12/20, mathastext has used *mathematically active*
  characters to propose certain advanced functionalities.  For reasons half
  lost in the mists of time but whose main one was surely to keep the
  meaning of the active shape of characters unchanged outside of math mode,
  this mathematical activation, and (in most cases) the definitions of what
  active characters do, were done again at *each* entrance into math mode.
  At this 1.4 release, mathastext does *not inject any code whatsoever* into
  the `\everymath` and `\everydisplay` toks registers anymore (*except* for
  one font-related hack needed under `LuaLaTeX`, see below).  Your documents
  will compile a tiny bit faster.

* In (*unsual*) documents where users play with catcodes and mathcodes it is
  *impossible* to keep exact backward compatibility, because documented user
  commands which acted formerly as toggles with delayed action now will enact
  changes immediately if in the document body.  In practice consequences are
  expected to be few, because catcode active characters are (as was already
  the case with earlier releases) hacked only when they are Babel shorthands
  and they are then modified in a way altering only their action in math
  mode.  The precise description of what mathastext does when mathematically
  activating (or not) a character, depending on circumstances, is to be
  found among small-print comments in the section "Extended scope of the
  math alphabets commands".  See also the documentation of the
  `\MTmathactiveletters` command for some specifics regarding ascii letters.

* New option: `everymath`. It instructs mathastext to revert (partially)
  to its legacy code which uses `\everymath/\everydisplay`.  This reversal
  is partial, the handling of ascii letters not being included into it.  The
  `everymath` option is there *only to try as a quick fix* in case transition
  to this release causes a major problem in a user document and time is
  lacking to investigate.  *Please report to the author such issues*.  Option
  `everymath` is destined to be removed at next major release.

* New option: `activedigits`.  Enjoy.

* It is now easier to hook into the mathastext architecture for
  mathematically activated ascii letters.  See the new section "Hacking
  letters (and even digits) for special tasks".

* Bugfix: do not override special behavior of the math mode dot in
  babel-spanish.

* Bugfix: A *desperate* hack related to `LuaLaTeX` font matters and dating
  back to 1.3o 2016/05/03 had been for some years in dire need of an update
  regarding fonts using `Renderer=HarfBuzz`.  This is done now.  Thanks to
  tex.sx `user691586` for report.  This is currently the sole remaining
  usage of `\everymath/\everydisplay`.

* Bugfix: `\MTexplicitbracesobeymathxx` (which is related to `\{` and `\}`)
  was without effect since an upstream `LaTeX` change at its 2020-02-02 release.

* With option symbolmisc, those math symbol macros formerly defined via
  `\DeclareRobustCommand` are now declared via `\protected\def`.

* Removal of legacy branches previously kept to support `LaTeX` earlier than
  2020-02-02.

* Removal of support for EU1 and EU2 font encodings.

* Option `noasterisk` deprecated at 1.2d 2013/01/02 has (finally) been removed.

* Four test files previously included and auto-extracted from the
  distributed dtx have been dropped.  One of them is still available
  on the package homepage.

* Some parts of the documentation have been massively re-ordered and even to some
  extent improved.  But there may be some occasions where obsolete statements will
  be found having the legacy `\everymath/\everydisplay` situation as background.

