Three main files are here.

Run the code in following order.

1. spn_cipher.py - This will encrypt a plaintext into a spn cipher. Block size for input is 16 bit and key size is also 16 bit. No of rounds will be 4.

2. linear_cryptanalysis.py - This will find a trail a between plain text and cipher text using a neural network also Linear approximation table will help to reduce error and find a equation which will help to do faster brute force on key as we will find subkey already.
Test data size will be 10000.

3. nn.py - A neural network which takes 16 bit input of block and predict a sub cipher after 3 round to help in satisying linear equation.

# Best result for trail

A neural network trained in such a way that it will try to predict subkey in the 3 round so that we can find a shortest and biased path reach to find round.

e.g. Through 3 rounds
      S_1,2: X1⊕X3⊕X4 = Y2, probBias = +4 (6,11 in LAT) (*1)
      S_2,2:    X2 = Y2⊕Y4, probBias = -4 (4,5 in LAT)  (*2)
      S_3,2:    X2 = Y2⊕Y4, probBias = -4               (*3)
      S_3,4:    X2 = Y2⊕Y4, probBias = -4               (*4)
      
