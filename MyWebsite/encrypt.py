import sys 
import sympy
import Witt as W 
import random

def stringfy(vector):
	s = ""
	for number in vector:		
		s += chr(number)
	return s
	
def encrypt(s):
	p = sympy.randprime(527,1000)
	
	vector = [ord(x) for x in s]
	
	key = [random.randint(0,p-1) for x in vector]
	
	encrypted = W.MittVector(vector,p) + W.MittVector(key,p)
	print(vector)
	print(key)
	print(encrypted)	
	
	encrypted_s, key = stringfy(encrypted.vector), stringfy(key)
		
	return encrypted_s,key + chr(p)
	
def decrypt(s,key):
	p = ord(key[-1])
	key = key[:-1]
	
	vector, key = [ord(x) for x in s], [ord(x) for x in key]
	
	decrypted = W.MittVector(vector,p) - W.MittVector(key,p)
	print(decrypted)
	return stringfy(decrypted.vector)
	
v = W.MittVector([3,3,3],5)
w = W.MittVector([2,3,4],5)
print(v,w,v+w)
print(W.MittVector([0,0,0],5)-w+w)
#print((v+w)-w)
#print(v + (w-w))
#print(w-w)
#print(v+W.WittVector([0,0,0],7))	

s = input("What is your message?")
new_s, key = encrypt(s)
print("Your encrypted message is:\n {} \n Your key is:\n {}".format(*encrypt(s)))

