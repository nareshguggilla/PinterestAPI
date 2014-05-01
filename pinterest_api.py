import json
from bottle import get, post, request, run
from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.mydatabase

@get('/')
def home():
    return "<h1>Welcome</h1><a href='/reg'>Register</a><br><a href='/login'>Login</a>"

@get('/reg')
def reg():
    return "<h1>Create Account</h1><form method='POST'><input type='text' name='name'>" + "<input type='text' name='username'>" + "<input type='password' name='password'>" + "<input type='submit' value='submit'></form>"

@post('/reg')
def reg():
    name = request.forms.get('name')
    username = request.forms.get('username')
    password = request.forms.get('password')
    user = { "name" : name, "username" : username, "password" : password}
    try:
        db['user'].save(user)
        return "<p>Account Created</p>"
    except ValidationError as ve:
        abort(400, str(ve))
    
@get('/login')
def get_login():
    return "<form method='POST'><input type='text' name='username'><input type='submit' value='submit'></form>"

@post('/login')
def login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    return "<p>Welcome " + username + "</p>" + "<a href='/resources'>Add Resource</a>"
    
@get('/resources')
def reg():
    resource_id = 123
    return "<a href='/resources/{resource_id}'>iPhone 5</a>"

@get('/resources/<resource_id>')
def reg(resource_id):
    return "<p>iPhone 5</p><a href='/add'>Add Resource</a>"

run()