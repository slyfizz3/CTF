enc="00 D2 FC D8 A2 DA BA 9E 9C 26 F8 F6 B4 CE 3C CC 96 88 98 34 82 DE 80 36 8A D8 C0 F0 38 AE 40 00".split(" ")
key=[]
for i in range(len(enc)):
	key.append(int(enc[i],16))
flag=""
for i in range(len(key)):
	for j in range(0x100):
		v5 = j
		v5 = (v5 >> 1) | (v5 << 7)
		v5&=0xff
		v5 ^= 0xef
		v5 = (v5 >> 2) | (v5 << 6)
		v5&=0xff
		v5 ^= 0xbe
		v5 = (v5 >> 3) | (32 * v5)
		v5&=0xff
		v5 ^= 0xed
		v5 = (v5 >> 4) | (16 * v5)
		v5&=0xff
		v5 ^= 0xde
		v5 = (v5 >> 5) | (8 * v5)
		v5&=0xff
		if v5==key[i]:
			flag+=chr(j)
			break
print(flag)