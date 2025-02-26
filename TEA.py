'''
Author: Michael Ptak
CS492 Homework 2 - TEA Implementation

Making it encode/decode a longer set of plaintext using CBC:
Encryption function:
    Take a random 64-bit IV (Initialization Vector)
    XOR the first plaintext block with the IV
    Encrypt the first block
    Use the previous output block as the IV for the next block
    Repeat for all blocks
Decryption Function: 
    Decrypt each ciphertext block
    XOR the result with the previous ciphertext block, or the IV if it is the first block.

'''
# Constants
DELTA = 0x9e3779b9
ROUNDS = 32

# Encryption
def encrypt(plaintext, key):
    # Convert the 128-bit key into four 32-bit integers
    K = [
        (key >> 96) & 0xFFFFFFFF, # K[0]
        (key >> 64) & 0xFFFFFFFF, # K[1]
        (key >> 32) & 0xFFFFFFFF, # K[2]
        (key) & 0xFFFFFFFF, # K[3]
    ]
    # Split 64-bit plaintext into L and R (32 bit halves)
    L = (plaintext >> 32) & 0xFFFFFFFF
    R = (plaintext) & 0xFFFFFFFF
    # Initialize sum
    sum = 0
    
    # Perform 32 rounds of encryption
    for i in range(ROUNDS):
        sum = sum + DELTA & 0xFFFFFFFF
        L = (L + (((R << 4) + K[0]) ^ (R+sum) ^ ((R >> 5) + K[1]))) & 0xFFFFFFFF
        R = (R + (((L << 4) + K[2]) ^ (L + sum) ^ ((L >> 5) + K[3]))) & 0xFFFFFFFF

    # Combine L and R to get the ciphertext, then return it
    ciphertext = (L << 32) | (R & 0xFFFFFFFF)
    return ciphertext

# Decryption
def decrypt(ciphertext, key):
    # Convert the 128-bit key into four 32-bit integers
    K = [
        (key >> 96) & 0xFFFFFFFF, 
        (key >> 64) & 0xFFFFFFFF, 
        (key >> 32) & 0xFFFFFFFF, 
        (key) & 0xFFFFFFFF, 
    ]
    # Split 64-bit ciphertext into L and R
    L = (ciphertext >> 32) & 0xFFFFFFFF
    R = (ciphertext) & 0xFFFFFFFF
    # Init sum
    sum = DELTA << 5 & 0xFFFFFFFF 

    # Perform 32 rounds of decryption
    for i in range(ROUNDS):
        R = (R - (((L << 4) + K[2]) ^ (L + sum) ^ ((L >>5) + K[3]))) & 0xFFFFFFFF
        L = (L - (((R << 4) + K[0]) ^ (R + sum) ^ ((R>>5) + K[1]))) & 0xFFFFFFFF
        sum = sum - DELTA & 0xFFFFFFFF

    # Combine L and R to get plaintext
    plaintext = (L << 32) | (R & 0xFFFFFFFF)
    return plaintext


# Testing
my_key = 0xAF6BABCDEF00F000FEAFAFAFACCDEF01 
my_plaintext = 0x01CA45670CABCDEF

print(f"Original CipherText: {my_plaintext}")
my_ciphertext = encrypt(my_plaintext, my_key)
print(f"CipherText (decimal): {my_ciphertext}")
print(f"Ciphertext (hex): {hex(my_ciphertext)}")
decrypted = decrypt(my_ciphertext, my_key)
print(f"Decrypted Plaintext: {decrypted}")