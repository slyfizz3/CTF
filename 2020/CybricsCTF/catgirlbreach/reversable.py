import struct
import ctypes
key=[168, 50, 186, 254]
def reversable(crypt,crown):
	MIO_MIC = ctypes.c_uint32(crypt[0])
	MIC_MIO = ctypes.c_uint32(crypt[1])
	CIU_CIO = 0x9e3779b8
	CIO_CIO=ctypes.c_uint32(-CIU_CIO*32)
	PINAY = 4
	PIYAU = 5
	VERSION_INFO = [0, 0]
	for i in range(32):
		CIO_CIO.value += CIU_CIO
		MIO_MIC.value += (MIC_MIO.value << PINAY) + crown[0] ^ MIC_MIO.value + CIO_CIO.value ^ (MIC_MIO.value >> PIYAU) + crown[1]
		MIC_MIO.value += (MIO_MIC.value << PINAY) + crown[2] ^ MIO_MIC.value + CIO_CIO.value ^ (MIO_MIC.value >> PIYAU) + crown[3]
	VERSION_INFO[0] = MIO_MIC.value
	VERSION_INFO[1] = MIC_MIO.value
	return VERSION_INFO

def WAKATTARA(crypt, key):
    crypt+= b"\x00"*( 8 - (len(crypt)%8))
    s = struct.Struct("<II")
    j = [(i[0], i[1]) for i in s.iter_unpack(crypt)]
    ans = []
    for block in j[0:]:
        clock = reversable(block, key)
        ans.append(clock)
    print(ans)
    return b"".join(struct.pack("<II", *i) for i in ans)

file=open("TOP SECRET FLAG.txt","rb").read()
out=WAKATTARA(file,key)
flag=''.join([chr(i)for i in out])
print(flag)
