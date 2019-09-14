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

It should be pointed out that few browsers as yet offer support for the kinds of OpenType 
*liga* features that the created fonts use. Firefox has offered such support for many
years now, but I have yet to see a version of Chrome that does.

### LibreOffice and Word

This has not been tested yet, but it should work in principle.

## Instructions

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

### Creating images

An image can be created from a fragment by:

```
create_image -f MyFont -s fontsize -o MyImage MyHieroglyphicEncoding
```

If omitted, the default font is `NewGardinerSMP.ttf`.
If omitted, the default fontsize is 20. 

### Examples

A number of example input files are provided in directory:

```
tests/
```

The following are examples of what can be run from the command-line with the
provided files:

```
analyze_font
analyze_font -f NewGardinerSMP
create_font -o tests/new tests/hieropage.html tests/hierotestsuite.html
create_font -f NewGardinerSMP -o tests/new tests/hieropage.html tests/hierotestsuite.html
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

## Installation

These instructions assume Linux.

### FontForge

FontForge is used to create composite glyphs. It is installed by:

```
apt-get install fontforge
apt-get install python-fontforge
```

### Python and AFDKO

At present both Python3 (for `analyze_font`) and Python2 (for `create_font`)
are required. 
The reason Python2 is still used is because Python3 is less easy to use
with the standard install of FontForge.

The Python scrips call `makeotf` from the command-line, which is part of AFDKO.

Assuming Python2 and Python3, and pip and pip3, are already installed,
then commands to install the necessary Python packages would typically be:

```
pip install -U ply
pip install -U Pillow
pip3 install -U afdko
```

On your platform, python2 and python3 may be called differently. Edit
`analyze_font` and `create_font` appropriately.

