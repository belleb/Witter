from flask import Flask, render_template, request  
import sympy, random
import Witt as W 
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/projects")
def projects():
    return render_template("projects.html")
    
@app.route("/projects/witter", methods=['GET', 'POST'])
def witter():
    if request.method == 'GET':
        return render_template("witter.html")

    def stringfy(vector):
        s = ""
        for number in vector:       
            s += chr(number)
        return s
    
    def isascii(s):
        try:
            s.encode("ascii")
            return True
        except:
            return False
    
    def encrypt(s):
        #if not isascii(s):
        #    return "Please use only ASCII characters", ":)"
        p = sympy.randprime(128,1000)
    
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
    
   
    
    s, k, decrypted = None, None, None 
    if "message" in request.form:
        s, k = encrypt(request.form["message"])
    
    if "key" in request.form and "encrypted" in request.form:
        decrypted = decrypt(request.form["encrypted"], request.form["key"])

    return render_template("witter.html",s=s,k=k,decrypted=decrypted)
    
if __name__ == "__main__":
    app.run(debug=True)