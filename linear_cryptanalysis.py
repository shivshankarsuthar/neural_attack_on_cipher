# This code will try to find a bias between a bias between plain text and cipher text , at the final
# we would try to guess some of subkey bits by doing using linear approximation

import spn_cipher as cipher
from math import fabs
import itertools as it
import collections


# this will inputs perameters for linear equation like a1,a2,a3 in a1*x1 + a2*x2 + a3*x3 = b1*y1 
sbox_input = ["".join(seq) for seq in it.product("01", repeat=4)]
# this will output perameters for linear equation like b1,b2 in a1*x1 + a2*x2 + a3*x3 = b1*y1 
sbox_output = [ bin(cipher.sbox[int(seq,2)])[2:].zfill(4) for seq in sbox_input ]
# create a table with input and output
sbox_b = collections.OrderedDict(zip(sbox_input,sbox_output))
# final linear approximation table initializing
bias = [[0 for x in range(len(sbox_b))] for y in range(len(sbox_b))] 

# here we will try to create a linear approximation table 
print('Linear Approximation Table: ')
for bits in sbox_b.items():
    input_bits, output_bits = bits
    temp = []
    for bit in [input_bits[0],input_bits[1],input_bits[2],input_bits[3]]:
        temp.append(int(bit,2))
    X1,X2,X3,X4 = temp
    
    temp = []
    for bit in [output_bits[0],output_bits[1],output_bits[2],output_bits[3]]:
        temp.append(int(bit,2))
    Y1,Y2,Y3,Y4 = temp

    equations_in = [0, X4, X3, X3^X4, X2, X2^X4, X2^X3, X2^X3^X4, X1, X1^X4,
                    X1^X3, X1^X3^X4, X1^X2, X1^X2^X4, X1^X2^X3, X1^X2^X3^X4] 
                    
    equations_out = [0, Y4, Y3, Y3^Y4, Y2, Y2^Y4, Y2^Y3, Y2^Y3^Y4, Y1, Y1^Y4,
                    Y1^Y3, Y1^Y3^Y4, Y1^Y2, Y1^Y2^Y4, Y1^Y2^Y3, Y1^Y2^Y3^Y4]                
    
    for x_idx in range (0, len(equations_in)):
        for y_idx in range (0, len(equations_out)):
            bias[x_idx][y_idx] += (equations_in[x_idx]==equations_out[y_idx])

# Print the linear approximation table
for bias in bias:
    for bia in bias:
        print('{:d}'.format(bia-8).zfill(2), end=' ')
    print('')


k = cipher.keyGeneration()
k_5 = int(k,16)&0xffff 
k_5_5_8 = (k_5>>8)&0b1111
k_5_13_16 = k_5&0b1111

print('\nTest key k = {:}'.format(k), end = ' ')
print( '(k_5 = {:}).'.format(hex(k_5).zfill(4)))
print('Targeting partial subkey K_5,5...k_5,8 = 0b{:} = 0x{:}'.format(bin(k_5_5_8)[2:].zfill(4), hex(k_5_5_8)[2:].zfill(1) ))
print('Targeting partial subkey K_5,13...k_5,16 = 0b{:} = 0x{:}'.format(bin(k_5_13_16)[2:].zfill(4), hex(k_5_13_16)[2:].zfill(1) ))
print('Testing each target subkey value...')

countTargetBias = [0]*256

for pt in range(10000):
    ct = cipher.encrypt(pt, k)
    ct_5_8 = (ct>>8)&0b1111
    ct_13_16 = ct&0b1111
    

    for target in range(256):
        target_5_8 = (target>>4)&0b1111
        target_13_16 = target&0b1111
        v_5_8 = (ct_5_8^target_5_8)
        v_13_16 = (ct_13_16^target_13_16)
		

	    # lets satisfy this equation
        u_5_8, u_13_16 = cipher.sbox_inv[v_5_8], cipher.sbox_inv[v_13_16]
        

        lApprox = ((u_5_8>>2)&0b1)^(u_5_8&0b1)^((u_13_16>>2)&0b1)^(u_13_16&0b1)^((pt>>11)&0b1)^((pt>>9)&0b1)^((pt>>8)&0b1)
        if lApprox == 0:
            countTargetBias[target] += 1

bias = [fabs(lAprx - 5000.0)/10000.0 for lAprx in countTargetBias]

maxResult, maxIdx = 0,0
for rIdx, result in enumerate(bias):
    if result > maxResult:
        maxResult = result
        maxIdx = rIdx

print('Highest bias is {:} for subKey value {:}.'.format(maxResult, hex(maxIdx)))
if (maxIdx>>4)&0b1111 == k_5_5_8 and maxIdx&0b1111 == k_5_13_16:
	print('Successfully got subkey')
else:
	print('Failure')



