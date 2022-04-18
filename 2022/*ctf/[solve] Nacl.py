def __ROL__(num, count, bits=32): 
	return ((num << count) | (num >> (bits - count))) & ((0b1<<bits) - 1) 
def __ROR__(num, count, bits=32): 
	return ((num >> count) | (num << (bits - count))) & ((0b1<<bits) - 1)

def enc1(x,y):
	word=[0x04050607, 0x00010203, 0x0C0D0E0F, 0x08090A0B, 0xCD3FE81B, 0xD7C45477, 0x9F3E9236, 0x0107F187, 0xF993CB81, 0xBF74166C, 0xDA198427, 0x1A05ABFF, 0x9307E5E4, 0xCB8B0E45, 0x306DF7F5, 0xAD300197, 0xAA86B056, 0x449263BA, 0x3FA4401B, 0x1E41F917, 0xC6CB1E7D, 0x18EB0D7A, 0xD4EC4800, 0xB486F92B, 0x8737F9F3, 0x765E3D25, 0xDB3D3537, 0xEE44552B, 0x11D0C94C, 0x9B605BCB, 0x903B98B3, 0x24C2EEA3, 0x896E10A2, 0x2247F0C0, 0xB84E5CAA, 0x8D2C04F0, 0x3BC7842C, 0x1A50D606, 0x49A1917C, 0x7E1CB50C, 0xFC27B826, 0x5FDDDFBC, 0xDE0FC404, 0xB2B30907]
	for i in range(44):
		a=(__ROL__(x,1))
		b=(__ROL__(x,8))
		c=(__ROL__(x, 2))
		d=((a&b)&0xffffffff^c)
		d^=y
		d^=word[i]
		y=x
		x=d
	return x,y

def rev1(x,y):
	word=[0x04050607, 0x00010203, 0x0C0D0E0F, 0x08090A0B, 0xCD3FE81B, 0xD7C45477, 0x9F3E9236, 0x0107F187, 0xF993CB81, 0xBF74166C, 0xDA198427, 0x1A05ABFF, 0x9307E5E4, 0xCB8B0E45, 0x306DF7F5, 0xAD300197, 0xAA86B056, 0x449263BA, 0x3FA4401B, 0x1E41F917, 0xC6CB1E7D, 0x18EB0D7A, 0xD4EC4800, 0xB486F92B, 0x8737F9F3, 0x765E3D25, 0xDB3D3537, 0xEE44552B, 0x11D0C94C, 0x9B605BCB, 0x903B98B3, 0x24C2EEA3, 0x896E10A2, 0x2247F0C0, 0xB84E5CAA, 0x8D2C04F0, 0x3BC7842C, 0x1A50D606, 0x49A1917C, 0x7E1CB50C, 0xFC27B826, 0x5FDDDFBC, 0xDE0FC404, 0xB2B30907]
	for i in range(43,-1,-1):
		d=x^word[i]
		a=(__ROL__(y,1))
		b=(__ROL__(y,8))
		c=(__ROL__(y, 2))
		o=(a&b)^c
		x=y
		y=o^d
	return x,y



def enc2(a1,a2,a3,a4):
	table=[a1,a2,a3]
	for i in range(a4):
		key=[0x03020100, 0x07060504, 0x0B0A0908, 0x0F0E0D0C, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000007]
		a=table[1]
		a<<=0x20
		eax=a>>32
		a1=(eax<<4)&0xffffffff
		a2=eax>>5
		c=a1^a2 
		eci=(c+eax)&0xffffffff
		dd=(key[table[0]&3]+table[0])&0xffffffff
		b=dd^eci
		table[2]=(table[2]+b)&0xffffffff
		table[0]+=(0x10325476)&0xffffffff

		tt=table[2]
		o=(tt<<4)&0xffffffff
		o2=tt>>5
		o3=o^o2
		b=(o3+table[2])&0xffffffff
		o4=(table[0]>>0xb)&3
		x=(table[0]+key[o4])&0xffffffff
		table[1]=(table[1]+(b^x))&0xffffffff
	return table

def rev2(a1,a2,a3,a4):
	ta=[a1,a2,a3]
	for i in range(a4):
		tt=ta[2]
		o=(tt<<4)&0xffffffff
		o2=tt>>5
		o3=o^o2
		b=(o3+ta[2])&0xffffffff
		key=[0x03020100, 0x07060504, 0x0B0A0908, 0x0F0E0D0C, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000007]
		o4=(ta[0]>>0xb)&3
		x=(ta[0]+key[o4])&0xffffffff
		ta[1]=(ta[1]-(b^x))&0xffffffff
		ta[0]=(ta[0]-0x10325476)&0xffffffff
		a=ta[1]
		a<<=0x20
		eax=a>>32
		a1=(eax<<4)&0xffffffff
		a2=eax>>5
		c=a1^a2 
		eci=(c+eax)&0xffffffff
		dd=(key[ta[0]&3]+ta[0])&0xffffffff
		b=dd^eci
		ta[2]=(ta[2]-b)&0xffffffff
	return ta

s=""
enc2=[0xFDF5C266, 0x7A328286, 0xCE944004, 0x5DE08ADC, 0xA6E4BD0A, 0x16CAADDC, 0x13CD6F0C, 0x1A75D936]


for i in range(4):
	enc=enc2[i*2:i*2+2]
	ta=rev2(0x10325476*pow(2,i+1),enc[1],enc[0],pow(2,i+1))
	ori1,ori2=rev1(ta[1],ta[2])
	s+=hex(ori1)[2:-1]
	s+=hex(ori2)[2:-1]

print("*CTF{"+s.decode("hex")+"}")
