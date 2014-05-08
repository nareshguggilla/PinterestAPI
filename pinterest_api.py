import StringIO
import json
import os
from bottle import get, post, delete, request, run

# Global Variables
global_user_id = 0
global_board_id = 0
global_pin_id = 0

# TODO: Connection to Datbase


###                                     ###                                  
#                                         #
#   Authentication (Registration, Login)  #
#                                         #
###                                     ###



###
#
#   Registration - Retrieves user's name, username, and password and stores them in DB
#   Input - name, username, password
#   Response - 200, success, user_id
#
# Registration
# To Test Use:
#   curl -X POST -H "Content-Type: application/json" -d '{"name":"xxxx","username":"xxxx","password":"xxxx"}' http://localhost:8080/v1/reg

@post('v1/reg')
def reg():
    r = json.load(request.body)
    name = r['name']
    username = r['username']
    password = r['password']
    
    # TODO: Enter user into database
    
    ### return user_id = gloabl_user_id
    user_id = global_user_id
    return { "success" : True, "status" : 201, "data" : { "user_id" : user_id }}

###
#
#   Login - Retrieves user's username and password and checks for user in DB
#   Input - username, password
#   Response - 200, success, user_id
#
# Registration
# To Test Use:
#   curl -X POST -H "Content-Type: application/json" -d '{"username":"xxxx","password":"xxxx"}' http://localhost:8080/v1/login

@post('v1/login')
def login():
    r = json.load(request.body)
    username = r['username']
    password = r['password']
    
    # TODO: Check user against database, verify credentials, and request user_id
    
    ### return user_id
    return { "success" : True, "status" : 200, "data" : { "user_id" : user_id }}




###                                         ###                                  
#                                             #
#   User Features (CRUD for boards and pins)  #
#                                             #
###                                         ###



###
#
#   Get User - Retrieves user info from DB
#   Input
#   Response - 200, success, user {name, boards[]}
#
# Get User
# To Test Use:
#   curl -X GET http://localhost:8080/v1/user/<user_id>

@get('/v1/user/<user_id>')
def get_user(user_id):
    return "It Worked" + user_id
    #based on userID, retreive name and boards list from DB
    #return response

###
#
#   Add Board - Creates a new board in the DB
#   Input - boardName, 
#   Response - 200, success, boardID
#
###
@post('/v1/user/<user_id>/board')
def add_board():
    return "Something"
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
@post('/v1/<user_id>/board/<board_id>')
def attach_pin():
    return "Something"
    #Retrieves board from DB
    #????? May include Pin info ?????
    #return response
    
###
#
#   Get Board - Get board from the DB
#   Input -  
#   Response - 200, success, board {boardName, pins[]}
#
###
@delete('/v1/<user_id>/board/<board_id>')
def delete_board():
    return "Something"
    #Retrieves board from DB
    #????? May include Pin info ?????
    #return response
    
###
#
#   Add Comment - Get board from the DB
#   Input -  
#   Response - 200, success, board {boardName, pins[]}
#
###
@delete('/v1/user/<userID>/pin/<pin_id>')
def delete_board():
    return "Something"
    #Retrieves board from DB
    #????? May include Pin info ?????
    #return response

# To Upload Using Curl
# curl --form upload=@localfilename --form press=OK [URL] 
@post('v1/user/<user_id>/pin/upload')
def upload():
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'

    save_path = "pins"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    upload.save(file_path)
    return "File successfully saved to '{0}'.".format(save_path)
    



###                                ###                                  
#                                    #
#   Public Access (boards and pins)  #
#                                    #
###                                ###



###
#
#   Get All Pins - Return all available Pins from DB
#   Input -  
#   Response - 200, success, pins[]
#

@get('/v1/pins')
def get_all_pins():
    return "Something"
    #Retrieves a list of all pins from DB
    #return response

###
#
#   Get a Pin - Get a Pin from the DB
#   Input -  pin_id
#   Response - 200, success, pin {pin_name, pin_url, comments[{ user, comment }]}
#

@get('/v1/pins/<pin_id>')
def get_pin(pin_id):
    return "Something"
    #Retrieves board from DB
    #????? May include Pin info ?????
    #return response
    
###
#
#   Get All Boards - Returns all available Boards from DB
#   Input -
#   Response - 200, success, boards[]
#

@post('/v1/boards')
def get_all_boards():
    return "Something"
    #Retrieves pin name and enters it into DB
    #????? How are we going to do the upload image part ?????
    #get pinID from newly created pin
    #return response
    
###
#
#   Get a Board - Get a Board from the DB
#   Input -  board_id
#   Response - 200, success, pins[{ pin_id, pin_name, pin_url }]
#

@get('/v1/boards/<board_id>')
def get_board(board_id):
    return "Something"
    #Retrieves pin from DB
    #return response
    
run(host='localhost', port=8080, debug=True)