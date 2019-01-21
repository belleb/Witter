from flask import Flask, render_template, request  
import sympy, random
import Witt as W 
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = False

block_len = 19
pre_key_len = 20
salt_len = 29
rabbit_shift = 127885

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/projects/")
def projects():
    return render_template("projects.html")
    
@app.route("/projects/witter/", methods=['GET', 'POST'])
def witter():
    if request.method == 'GET':
        return render_template("witter.html")

    def stringfy(vector):
        s = ""
        for number in vector:       
            s += chr(number)
        return s
    
    def allowed_letters(s):
        for letter in s:
            if ord(letter)>=350:
                return False
        return True
        
            
    def rabbitfy(s):
        rabbit_s = ""
        for letter in s:
            rabbit_s += chr(ord(letter) + rabbit_shift)
        return rabbit_s
            
    def unrabbitfy(s):
        unrabbit_s = ""
        for letter in s:
            if ord(letter) >= rabbit_shift:
                unrabbit_s += chr(ord(letter) - rabbit_shift)
        return unrabbit_s
    
    def small_encrypt(vector,key,p):
        encrypted = W.WittVector(vector,p) + W.WittVector(key,p)
        return rabbitfy(stringfy(encrypted.vector))
        
    def small_decrypt(vector,key,p):
        decrypted = W.WittVector(vector,p) - W.WittVector(key,p)
        return stringfy(decrypted.vector)
        
    def encrypt(s):
        if not s:
            return "Please write some message!", ":)"
        if not allowed_letters(s):
            return "Please use only ASCII characters", ":)"
       
        p = sympy.randprime(350,445)
    
        vector = [ord(x) for x in s]
        pre_key = [random.randint(33,126) for i in range(pre_key_len)]
        key = []
        for i in range(len(vector)):
            key.append(pre_key[i % pre_key_len]+(i % salt_len))
         
        encrypted_s = ""   
        for i in range(0,len(vector),block_len):
            small_vector = vector[i: i+block_len]
            small_key = key[i: i+block_len]
            small_encrypted = small_encrypt(small_vector,small_key,p)
            encrypted_s += small_encrypted
            
  
        pre_key = stringfy(pre_key)+chr(p-320)
        
        return encrypted_s,pre_key 
    
    def decrypt(s,key):
        s = unrabbitfy(s)
        if not s:
            return "Where is your encrypted message?"
        key = key.strip()
        if len(key)!=pre_key_len+1:
            return "Don't forget your decryption key!"
        p = (ord(key[-1])+320 )%445
        pre_key = key[:-1]
        
        
        vector, pre_key = [ord(x) for x in s], [ord(x) for x in pre_key]
        key = []
        for i in range(len(vector)):
           key.append(pre_key[i % pre_key_len]+(i % salt_len))
           
        decrypted = ""   
        for i in range(0,len(vector),block_len):
            small_vector = vector[i: i+block_len]
            small_key = key[i: i+block_len]
            small_decrypted = small_decrypt(small_vector,small_key,p)
            decrypted += small_decrypted
           
        
        return decrypted
    
   
    
    s, k, decrypted = "", "", ""
    if "message" in request.form:
        s, k = encrypt(request.form["message"])
    
    if "key" in request.form and "encrypted" in request.form:
        decrypted = decrypt(request.form["encrypted"], request.form["key"])

    return render_template("witter.html",s=s,k=k,decrypted=decrypted)
    
if __name__ == "__main__":
    app.run(debug=True)