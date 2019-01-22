from flask import Flask, render_template, request  
import sympy, random
import Witt as W 
from crypto import *

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = False


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
    
    s, k, decrypted = "", "", ""
    if "message" in request.form:
        s, k = encrypt(request.form["message"])
    
    if "key" in request.form and "encrypted" in request.form:
        decrypted = decrypt(request.form["encrypted"], request.form["key"])

    return render_template("witter.html",s=s,k=k,decrypted=decrypted)
    
if __name__ == "__main__":
    app.run(debug=True)