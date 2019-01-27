#!/usr/bin/env python3

import sys
import base64

def base64_image(filename):
    try:
        data = open(filename, 'rb').read()
        return base64.b64encode(data)
    except:
        print("Problem reading " + filename + " :(")
        sys.exit(2)

def read_js(filename):
    try:
        return open(filename, 'rb').read()
    except:
        print("Problem reading " + filename + " :(")
        sys.exit(3)

def add_xref_table(pdf):
    done = False
    offsets = []
    i = 1
    while not done:
        try:
            offset = pdf.index(bytes(str(i) + " 0 obj", "ascii"))
            offsets.append(offset)
            i += 1
        except:
            done = True
    xref = b"xref\n0 " + bytes(str(len(offsets) + 1), "ascii") + b"\n0000000000 65535 f\r\n"
    xref += b''.join([b"%010d %05d n\r\n" % (o, 0) for o in offsets])
    pdf = pdf.replace(b"trailer", xref + b"trailer")
    xref_index = pdf.index(b"xref\n")
    pdf = pdf.replace(b"%%EOF", b"startxref\n" + bytes(str(xref_index), "ascii") + b"\n%%EOF")
    return pdf

if len(sys.argv) != 5:
    print("Usage: jhpdf.py jekyll.jpg hyde.jpg condition.js output.pdf")
    sys.exit(1)

jekyll    = sys.argv[1]
hyde      = sys.argv[2]
condition = sys.argv[3]
output    = sys.argv[4]

# read in XFA template and put base64-encoded images at the correct place
xfa = open('xfa_template.xml', 'rb').read()
jekyll_b64 = base64_image(jekyll)
hyde_b64   = base64_image(hyde)
xfa = xfa.replace(b'[[IMG1]]', jekyll_b64).replace(b'[[IMG2]]', hyde_b64)

# read PDF template and insert JS code
pdf = open('pdf_template.pdf', 'rb').read()
js = read_js(condition)
pdf = pdf.replace(b'[[JS]]', js)

# insert XFA into PDF and add xref table
pdf = pdf.replace(b'[[XFA_LEN]]', bytes(str(len(xfa)), 'ascii')) \
         .replace(b'[[XFA]]', xfa)
pdf = add_xref_table(pdf)

try:
    open(output, 'wb').write(pdf)
except:
    print("Problem writing " + output + " :(")
    sys.exit(4)
