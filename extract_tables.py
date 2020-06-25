import sys
import struct

if len(sys.argv)>=2:
  if len(sys.argv[1])>=1:
    f = open(sys.argv[1] + ".ttx","r")
    latest_tag = ""
    if (f):
      in_hex_data = False
      for s in f:
        if not in_hex_data:
          if s.find("<hexdata")>=0:
            in_hex_data=True
            f2 = open(sys.argv[1] + "-" + latest_tag + ".bin","w")
          elif len(s.strip())>0:
            if s.strip()[0]=="<":
              latest_tag = (s.strip()[1:]).split()[0]
        else:
          if s.find("</hexdata")>=0:
            f2.close()
            in_hex_data=False
          else:
            print s
            x = s.split()
            for y in x:
              while len(y)>=2:
                f2.write(struct.pack('B', int(y[0:2], 16)))  # 'B' = unsignd char
                y = y[2:]    # Remove the first 2 hex digits
      f.close()
