# SPN is a cipher with 16 bit input and 16 bit output and goes through 4 rounds.

import random
import hashlib
from boxes import *

blockSize = 16
verboseState = False

# We have four rounds and we need 5 keys , for this we will create 16 bit long keys. SHA1 is 128 bit long we will take
# only 20 digit of hexdecial so it will becomde 20*4 = 80 bit which will give 16 * 5 keys.
def keyGeneration():
    k = hashlib.sha1( hex(random.getrandbits(128)).encode('utf-8') ).hexdigest()[2:2+20]
    return k

# this is main function which will encrypt plain text in cipher text
# We will encrypt upto 3 Rounds first then we will encrypt last round manually because it will help us to use linear approximation attack in later.
def encrypt(pt, k):
    cipherState = pt
    if verboseState: print('**pt = {:04x}**'.format(cipherState))
    
    subKeys = [ int(subK,16) for subK in [ k[0:4],k[4:8], k[8:12], k[12:16], k[16:20] ] ]
    
    
    for roundN in range(0,3):
    
        if verboseState: print(roundN, end = ' ')
        # XOR operation between key and subcipher
        cipherState = cipherState^subKeys[roundN]
        if verboseState: print (hex(cipherState), end = ' ')
        
      
        cipherState = Sbox(cipherState,sbox)
        if verboseState: print (hex(cipherState), end = ' ')
        
      
        state_temp = 0      
        for bitIdx in range(0,blockSize):
            if(cipherState & (1 << bitIdx)):
                state_temp |= (1 << pbox[bitIdx])
        cipherState = state_temp
        if verboseState: print (hex(cipherState))
    
    # final round
    cipherState = cipherState^subKeys[-2] # key mixing
    if verboseState: print (str(3), hex(cipherState), end = ' ')   
    cipherState = Sbox(cipherState,sbox)
    if verboseState: print (hex(cipherState), end = ' ')
    cipherState = cipherState^subKeys[-1] # final key mixing
    if verboseState: print (hex(cipherState)) 
    if verboseState: print('**ct = {:04x}**'.format(cipherState))
    
    return cipherState


if __name__ == "__main__":
    
   
    k = keyGeneration()
    # creating dataset
    fileName = 'testData/'  + 'test1' +'.dat'
    nVals = 10000
    fd_w = open(fileName,"w")
    print ('Key = {:}'.format(k))
    
    #fd_w.write('test')
    fd_w.write(k+'\n')
    for i in range(0, nVals):     
        fd_w.write('{:04x},{:04x}\n'.format(i, encrypt(i, k)))
    
    fd_w.close()
    
    print ('Simple SPN plaintext, ciphertext data written to testData/test1 ' + fileName) 
    print ('{:} values written.'.format(nVals))
    
                 
