# Jekyll and Hyde PDF generator

Generate PDF files which based on a JavaScript condition show one of two
images.

## Usage

./jhpdf.py jekyll.jpg hyde.jpg condition.js output.pdf

## Example

./jhpdf.py examples/img/Dr_Jekyll.jpg examples/img/Mr_Hyde.jpg examples/random_condition.js jh.pdf && acroread jh.pdf

This generates a PDF file which randomly either shows Dr. Jekyll or Mr. Hyde.

## Background

For a background blog post, see https://shiftordie.de/blog/2019/01/27/the-jekyll-and-hyde-pdf/
