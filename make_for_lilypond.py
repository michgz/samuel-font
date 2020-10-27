from sys import argv
from fontforge import *
import os
import re

# Write to a log
fd = os.open('log.txt', os.O_WRONLY)
with os.fdopen(fd, 'w') as f4:
  for i in range(len(argv)):
    f4.write("%s\n" % argv[i])

# Create the "first pass" output
h=fontforge.open('samuel-11.sfd')
h.generate('samuel-11-temp.otf')

# Dump to text form
os.system('fonttools ttx -o sam.ttx samuel-11-temp.otf')

# Read in and process the dumped data

def make_LILY(sz):
  s = ''
  s += '(staffsize . {0:f})\n'.format(float(sz))
  s += '(stafflinethickness . {0:f})\n'.format(0.5)
  s += '(staff_space . {0:f})\n'.format(2.6*float(sz))
  s += '(linethickness . {0:f})\n'.format(0.5)
  s += '(black_notehead_width . {0:f})\n'.format(8.0)
  s += '(ledgerlinethickness . {0:f})\n'.format(1.0)
  s += '(design_size . {0:f})\n'.format(float(sz))
  s += '(blot_diameter . {0:f})\n'.format(0.4)
  return s
  
def make_LILF(sz):
  s = ''
  s += 'feta{0} '.format(sz)
  s += 'feta-noteheads{0} '.format(sz)
  s += 'feta-flags{0} '.format(sz)
  s += 'parmesan{0} '.format(sz)
  s += 'parmesan-noteheads{0} '.format(sz)
  s += 'feta-alphabet{0}'.format(sz)
  return s

def make_LILC(sz, c):
  s = ''
  s += '({0} .\n'.format(c['name'])
  s += '((bbox . ({0:f} {1:f} {2:f} {3:f}))\n'.format(0.0,0.0,0.0,0.0)
  #s += '(subfont . "feta-alphabet{0}")\n'.format(sz)
  s += '(subfont . "feta-noteheads{0}")\n'.format(sz)
  s += '(subfont-index . {0})\n'.format(c['id'])
  s += '(attachment . ({0:f} . {1:f}))))\n'.format(0.0,0.0)
  return s


INPUT_NAME = 'sam.ttx'
c = {}

fd = os.open(INPUT_NAME, os.O_RDONLY)
with os.fdopen(fd, 'r') as f2:
  for s in f2:
    if s.find("<GlyphID")>=0:
      # Use regular expressions
      r=re.search("(id=\".*?\") (name=\".*?\")",s)
      if (r!=None and len(r.groups())>=2):
        id_1=int(r.group(1)[4:len(r.group(1))-1])
        name=r.group(2)[6:len(r.group(2))-1]
        if name in c:
          c[name]["glyphid"]=id_1
        else:
          c[name]={}
          c[name]["glyphid"]=id_1

    elif s.find("<mtx")>=0:
      # Use regular expressions
      r=re.search("(name=\".*?\") (width=\".*?\") (lsb=\".*?\")",s)
      if (r!=None and len(r.groups())>=3):
        name=r.group(1)[6:len(r.group(1))-1]
        width=int(r.group(2)[7:len(r.group(2))-1])
        lsb=int(r.group(3)[5:len(r.group(3))-1])
        d = {'width':width, 'lsb':lsb}
        if name in c:
          c[name]["mtx"]=d
        else:
          c[name]={}
          c[name]["mtx"]=d

    elif s.find("<ClassDef")>=0:
      # Use regular expressions
      r=re.search("(glyph=\".*?\") (class=\".*?\")",s)
      if (r!=None and len(r.groups())>=2):
        name=r.group(1)[7:len(r.group(1))-1]
        class_1=int(r.group(2)[7:len(r.group(2))-1])
        if name in c:
          c[name]["classdef"]=class_1
        else:
          c[name]={}
          c[name]["classdef"]=class_1


# Now do the second pass generation
for INPUT_SIZE in [11, 13, 14, 16, 18, 20, 23, 26]:

  h=fontforge.open('samuel-11.sfd')

  h.setTableData("LILY", make_LILY(INPUT_SIZE))
  h.setTableData("LILF", make_LILF(INPUT_SIZE))

  s = ''
  i = 0
  for cc in c:
    i += 1
    d = {'name': cc, 'id': i}
    s += make_LILC(INPUT_SIZE, d)
  h.setTableData("LILC", s)

  h.generate('samuel-{0}.otf'.format(INPUT_SIZE))

