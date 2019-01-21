powers_of_p = {}
def p_pow(p, i):
	if (p,i) not in powers_of_p:
		if i == 0:
			powers_of_p[p,i] = 1
		else:
			powers_of_p[p,i] = p_pow(p, i-1)*p
	return powers_of_p[p,i]


class WittVector:
	
	def __init__(self, vector, p):
		self.vector = [x % p for x in vector]
		self.p = p
	
	def __str__(self):
		return str(self.vector)
		
	def __len__(self):
		return len(self.vector)
		
	def __getitem__(self,key):
		return self.vector[key]	
			
	def __add__(self, w):
		if self.p != w.p:
			raise Exception("Witt vectors of different types")
			
		else:
			return WittVector(self.S(len(self)-1,w), self.p)
	
	def __neg__(self):
		return WittVector([-x for x in self.vector], self.p)

	def __sub__(self, w):
	    return WittVector((self+(-w)).vector,self.p)
	
		
	def S(self,n,w):
		p = self.p		
		if n == 0:
			return [(self[0] + w[0])%p]			
		
		previous_S = self.S(n-1,w)	
		S_n_term = ((self.ghost(n) + w.ghost(n) - WittVector(previous_S,self.p).almost_ghost(n-1))//p_pow(p,n))  %p
		previous_S.append(S_n_term)
		
		return previous_S
		  
	def ghost(self,n):
		p = self.p
		output = 0
		for i, x in enumerate(self.vector):
			if i < n + 1:
				output = (output + pow(x,(p_pow(p, n-i)),p_pow(p,n+2))*p_pow(p,i)) 
		return output
		
	def almost_ghost(self,n):
		p = self.p
		output = 0
		for i, x in enumerate(self.vector):
			if i < n + 1:
				output = (output + pow(x,p_pow(p,n+1-i),p_pow(p,n+2))*(p_pow(p,i)))
		return output

	