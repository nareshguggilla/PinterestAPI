from bottle import get, post, request, run

###
#
#   Registration - Retrieves user's name, username, and password and stores them in DB
#   Input - name, username, password
#   Response - 200, success, userID
#
###
@post('/v1/reg')
def home():
    #get post data and create a user object
    name = request.forms.get('name')
    username = request.forms.get('username')
    password = request.forms.get('password')
    user = { "name" : name, "username" : username, "password" : password}
    
    #put user in database
    #get userID from newly created user
    #return response

###
#
#   Login - Retrieves user's username and password and checks for user in DB
#   Input - username, password
#   Response - 200, success, userID
#
###
@post('/v1/login')
def login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    #check credentials against DB
    #get userID if credentials clear
    #return response
    
###
#
#   Get User - Retrieves user info from DB
#   Input
#   Response - 200, success, user {name, boards[]}
#
###
@get('/v1/<userID>')
def get_user():
    
    #based on userID, retreive name and boards list from DB
    #return response
    
###
#
#   Add Board - Creates a new board in the DB
#   Input - boardName, 
#   Response - 200, success, boardID
#
###
@post('/v1/<userID>/board')
def add_board():
    
    #Retrieves board name and enters it into DB
    #get boardID from newly created board
    #return response
    
###
#
#   Get Board - Get board from the DB
#   Input -  
#   Response - 200, success, board {boardName, pins[]}
#
###
@get('/v1/<userID>/board/<boardID>')
def get_board():
    
    #Retrieves board from DB
    #????? May include Pin info ?????
    #return response
    
###
#
#   Add Pin - Creates a new pin in the DB, includes upload of image to file system
#   Input - pinName, pinURL
#   Response - 200, success, pinID
#
###
@post('/v1/<userID>/board/<boardID>/pin')
def add_pin():
    
    #Retrieves pin name and enters it into DB
    #????? How are we going to do the upload image part ?????
    #get pinID from newly created pin
    #return response
    
###
#
#   Get Pin - Get pin from the DB
#   Input -  
#   Response - 200, success, pin {pinName, pinURL, comments[]}
#
###
@get('/v1/<userID>/board/<boardID>/pin/<pinID>')
def get_board():
    
    #Retrieves pin from DB
    #return response

run()