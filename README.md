# Generation of OpenType fonts for Ancient Egyptian hieroglyphic text

Use of the code here is appropriate under the following circumstances:

1. There is a relatively stable set of documents with (Unicode) encoding of Ancient
Egyptian hieroglyphic text.

2. The documents explicitly activate a named OpenType font for the
occurrences of fragments of Ancient Egyptian.

The reason why a stable set of documents is a requirement is that the font
will not be able to handle anything that does not occur in the given documents. 
For every added fragment, the font needs to be recreated.

For frequently changing documents that include hieroglyphic text consider the
[alternative in pure JavaScript](https://github.com/nederhof/resjs).

## Different kinds of use

### Use on the web

One can create one or more webpages that include fragments of Ancient Egyptian, using CSS
to select a font for these fragments. By running a script on these webpages,
the required font is created.

At this time, not all browsers may realize the kinds of OpenType *liga* features 
that the created fonts use. 

### LibreOffice and Word

This is left for future development. This should work in principle,
as long as one can obtain a text file that has fragments of hieroglyphic as substrings.
The most suitable format seems "Flat XML ODF".

## Installation

These instructions assume Linux.

### FontForge

FontForge is used to create composite glyphs. On Debian-based Linux it is installed by:

```
apt-get install fontforge
apt-get install python-fontforge
```

On Fedora, it would reportedly just be:

```
yum install fontforge
```

### Python and AFDKO

It should be possible to run this code with just Python3.
On some distributions however, FontForge is not yet available for Python3, in
which case Python2 should be used to run `create_font`.

The Python scripts call `makeotf` from the command-line, which is part of AFDKO.

Assuming Python and pip are already installed,
then commands to install the necessary Python packages would typically be:

```
pip install -U ply
pip install -U Pillow
pip install -U afdko
```

On your platform, python2 and python3 may be called differently. If so, edit
the first line of `analyze_font`, `create_font` and `create_image` appropriately.

## Running

### Adding a new font

One TTF font, `NewGardinerSMP.ttf`, is available in the directory:

```
fonts/
```

This is the default font.

To add another TTF font, say `MyFont.ttf`, put it in the same directory,
and execute:

```
analyze_font -f MyFont
```

This analyzes the font, and puts the result of this analysis in a `.json` file
in the same directory.

A suitable font should have the following requirements:

1. It should contain glyphs for all hieroglyphs from `0x13000` to `0x1342e` and
for the control characters from `0x13430` to `0x13438`.

2. The glyphs should rest on the baseline.

### Creating a font for a number of documents

To create a font for a collection of files `file1`, `file2`, ..., containing fragments of
hieroglyphic encoding, which would typically be .html or .txt files, do:


```
create_font -o OutFont file1 file2 ...
```

Here `OutFont.otf` will be put in the directory from where `create_font` is
called.

To use a custom font, say `MyFont.ttf`, rather than the default font, do:

```
create_font -f MyFont -o OutFont file1 file2 ...
```

By adding the `-c` flag, one ensures that the created font includes every
hieroglyph. In this way, each fragment of hieroglyphic encoding in every document 
is visible if viewed with that font, even though some groups may not be properly formatted.
For example:

```
create_font -o OutFont -c file1 file2 ...
```

### Adding custom groups

To interpret control characters in a non-standard way, one can
compile a list of custom groups in a plain text file. Each line in that file consists of
a source sequence of characters (two or more), a space or tab, 
and a target sequence of characters (one or more) composed using control characters.
The characters in both sequences may be written as HTML entities.

A file of custom groups is preceded by the `-g` flag:

```
create_font -g CustomGroups -o OutFont file1 file2 ...
```

The source sequences need not contain control characters. By mapping them to
target sequences with control characters,
a webpage containing bare sequences of hieroglyphs can be rendered as 
if it had control characters.

It is important to realize that a custom group may not lead to the desired
result if it is a subgroup of a larger group with control characters in one of the input files;
i.e. the target sequence will not be recognized as part of the larger group.
A more typical use would therefore be with the `-c` flag and without input
files `file1 file 2 ...`.

### Creating images

An image can be created from a fragment by:

```
create_image -f MyFont -s fontsize -o MyImage MyHieroglyphicEncoding
```

If omitted, the default font is `NewGardinerSMP.ttf`.
If omitted, the default fontsize is 20. 
The hieroglyphic encoding may contain HTML entities for hieroglyphs and
control characters, which are replaced by characters.

### Examples

A number of example input files are provided in directory:

```
tests/
```

This includes an OpenType font that was generated with the tools presented
here. Two HTML files can be viewed with a browser.

The following are examples of what can be run from the command-line with the
provided files:

```
analyze_font
analyze_font -f NewGardinerSMP
create_font -o tests/new tests/hieropage.html tests/hierotestsuite.html
create_font -f NewGardinerSMP -o tests/new -c tests/hierotestsuite.html
create_image -o myimage.jpg "&#x1340d;&#x13431;&#x1340d;&#x13430;&#x1340d;"
```

One can call `create_font` from another directory, e.g.:

```
cd tests
../create_font -o new hieropage.html hierotestsuite.html
```

or

```
../create_font -f NewGardinerSMP -o new hieropage.html hierotestsuite.html
```

This creates a font `new.otf` in the `tests/` directory.

An example with custom groups:

```
../create_font -g customgroups.txt -o new customgroups.html
```
