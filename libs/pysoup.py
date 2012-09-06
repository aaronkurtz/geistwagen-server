import struct

def readByte(data):
  return struct.unpack('B',data) 

def readShort(data):
  b1,b2 = struct.unpack('BB',data)
  return (b1 << 8) | (b2 & 0x00FF)

def readInt(data):
  b1,b2,b3,b4 = struct.unpack('BBBB',data)
  data = (b1 >> 24) | ((b2 & 0x000000FF) >> 16) 
  data |= ((b3 & 0x000000FF) << 8) | (b4 & 0x000000FF);
  return data;

def readString(data, len):
  pass

def verify_bones_file(data):
    checksum = 0xDC55 #Crawl signature
    header = data[0:20]
    payload = data[20:]
    majorVersion = readByte(header[0])
    minorVersion = readByte(header[1])
    if readShort(header[2:4]) != checksum:
     return False #Lacks crawl signature
    if readInt(header[16:20]) != len(payload):
     return False #Ghost(s) tag is improper
    return True
#TODO: check against game logic - no 9 XL 27 SpFEs on level 3

def load_file(bones): 
  with open(bones,mode='rb') as file:
    data = file.read()
  return data    

def check_bones(bones):
    data = load_file(bones)
    if verify_bones_file(data):
        print "Proper Stone Soup bone file"
    else:
        print "Bad file"
