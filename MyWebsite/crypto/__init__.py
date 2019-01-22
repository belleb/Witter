"""
This package contains the functions used to encrypt and decrypt
"""
import sympy, random
import Witt as W 
"""
Since the time complexity of computations with Witt vectors is high, we break the message in blocks of fixed length (block_len)

pre_key_len is the length of the basic key. We make this key into a large key of the same size of the message by using some 
modified repetition which is controlled by salt_len. 

min_pre_key_len sets the minumum length for a key entered by the user

rabbit_shift shifts the order of the characters in the encrypted message by a constant, making the final result look like a sequence of emoticons. 
"""
block_len = 19
pre_key_len = 20
salt_len = 29
rabbit_shift = 127744 #885
min_pre_key_len = 8
#lower and upper bounds for prime p
lb_p = 350
ub_p = 1235 #1585

#transforms an int array into a string by using chr
def stringfy(vector):
    s = ""
    for number in vector:       
        s += chr(number)
    return s

#tests if the user inserted only allowed characters in their message
def allowed_letters(s):
    for letter in s:
        if ord(letter)>=lb_p:
            return False
    return True
    
#shifts message to the "emoticon zone".        
def rabbitfy(s):
    rabbit_s = ""
    for letter in s:
        rabbit_s += chr(ord(letter) + rabbit_shift)
    return rabbit_s
        
#shifts message back from "emoticon zone". Also removes spaces, correcting user mistakes.          
def unrabbitfy(s):
    unrabbit_s = ""
    for letter in s:
        if ord(letter) >= rabbit_shift:
            unrabbit_s += chr(ord(letter) - rabbit_shift)
    return unrabbit_s

#encrypts a block of small size
def small_encrypt(vector,key,p):
    encrypted = W.WittVector(vector,p) + W.WittVector(key,p)
    return rabbitfy(stringfy(encrypted.vector))
    
#decrypts a block of small size
def small_decrypt(vector,key,p):
    decrypted = W.WittVector(vector,p) - W.WittVector(key,p)
    return stringfy(decrypted.vector)

#creates a key for the user, in case the user did not enter their own key or entered an invalid key
def create_key(size, pre_key_len, salt_len):
    #creates a short pre_key of size pre_key_len
    pre_key = [random.randint(33,126) for i in range(pre_key_len)]
    
    
    #adapts pre_key to actual key that has the same size as the message
    key = []
    for i in range(size):
        key.append(pre_key[i % pre_key_len]+(i % salt_len)+(sum(pre_key)%salt_len))
    
    return key, pre_key
    
#adapts key entered by user into a usable cryptographic key
def adapt_key(size, pre_key_len, salt_len, key): 
    #adapts entered key to a int array pre_key of size pre_key_len
    pre_key = key[:pre_key_len]
    pre_key = [ord(x) for x in pre_key]
    
    i, l = len(pre_key)-1, len(pre_key)
    while i < pre_key_len - 1:
        i += 1
        pre_key.append(pre_key[i%l] + (i% salt_len))
    
    #constructs actual key that has the same size as the message
    key = []
    for i in range(size):
        key.append(pre_key[i % pre_key_len]+(i % salt_len)+(sum(pre_key)%salt_len))
    
    return key    

#encrypts whole message. The user can choose to use their own key or receive a random key
def encrypt(s, key=""):
    if not s:
        return "Please write some message!", chr(128578) 
        
    if not allowed_letters(s):
        return "Please use only ASCII characters", chr(128578) 
    
    #constructs crypto key and an "user_key" to be show to the user. If the user chose their own key, a message is shown instead
    if len(key) < min_pre_key_len or not allowed_letters(key): 
        key, user_key = create_key(len(s), pre_key_len, salt_len)
        user_key = stringfy(user_key)
    else:
        key = adapt_key(len(s), pre_key_len, salt_len, key)
        user_key = "Don't forget your chosen key " + chr(128578)
        
    #generated random prime p. We will use p-typical Witt vectors 
    p = sympy.randprime(lb_p,ub_p)


    #encrypts message
    vector = [ord(x) for x in s]
    encrypted_s = ""   
    
    for i in range(0,len(vector),block_len):
        small_vector = vector[i: i+block_len]
        small_key = key[i: i+block_len]
        small_encrypted = small_encrypt(small_vector,small_key,p)
        encrypted_s += small_encrypted
        

        
    #encodes the random prime together with the encrypted message
    encrypted_s += chr(p+127394)
         
    return encrypted_s, user_key 

#find prime p using the encrypted message. If the prime is not in the allowed range, returns None
def find_prime(s):
    prime_char = s[-1]
    p = ord(prime_char)
    if p > 127394:
        p -= 127394
    
    if p in range(lb_p,ub_p): 
        return p
    else:
        return None

#decrypts          
def decrypt(s,key):
    #deletes spaces at the ends, and tests if the message and key look right
    s, key = s.strip(), key.strip()
    if not s:
        return "Where is your encrypted message?"
    
    if len(key) < min(pre_key_len, min_pre_key_len):
        return "Don't forget your decryption key!"
    
    p = find_prime(s)
    s = unrabbitfy(s[:-1])
    if not p or not s:
        return "Something looks wrong..."
     
    #creates usable key and an array representing the encrypted message 
    key = adapt_key(len(s), pre_key_len, salt_len, key) 
    vector = [ord(x) for x in s]
    
    #decrypts   
    decrypted = ""   
    for i in range(0,len(vector),block_len):
        small_vector = vector[i: i+block_len]
        small_key = key[i: i+block_len]
        small_decrypted = small_decrypt(small_vector,small_key,p)
        decrypted += small_decrypted
       
    
    return decrypted