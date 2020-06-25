import sys
import struct

def implant(f_i,f_o):
  i = 0
  while(True):
    chunk = f_i.read(1)
    if chunk == '':
      break
    if (i == 0):
      f_o.write("      ")
    elif ((i%4)==0):
      f_o.write(" ")
    f_o.write("%02x" % struct.unpack('B', chunk[0]))
    if (i >= 15):
      f_o.write("\n")
      i = 0
    else:
      i = i + 1
  if i != 0:
    f_o.write("\n")



if len(sys.argv)>=2:
  if len(sys.argv[1])>=1:
    f7 = open("11-template.ttx","r")
    if (f7):
      f8 = open(sys.argv[1] + "-new.ttx","w")
      if (f8):
        for s in f7:
          if s.find("%CURRENTDATETIME%")>=0:
            f8.write(s.replace("%CURRENTDATETIME%", "Thu Feb 12 20:54:29 2015"))
          elif s.find("%POINTSIZE%")>=0:
            f8.write(s.replace("%POINTSIZE%", sys.argv[1]))
          elif s.find("%HEX_LILC%")>=0:
            f9 = open(sys.argv[1] + "-LILC.bin","r")
            implant(f9,f8)
            f9.close()
          elif s.find("%HEX_LILF%")>=0:
            f9 = open(sys.argv[1] + "-LILF.bin","r")
            implant(f9,f8)
            f9.close()
          elif s.find("%HEX_LILY%")>=0:
            f9 = open(sys.argv[1] + "-LILY.bin","r")
            implant(f9,f8)
            f9.close()
          else:
            f8.write(s)
        f8.close()
      f7.close()
