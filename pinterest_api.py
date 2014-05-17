import functions
import json
import os.path
from bottle import get, post, delete, request, run


functions.setup()

#   Root Path /  #
@get('/')
def base():
    return 'PinterestAPI'

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

@post('/v1/reg')
def reg():
    #print request.body
    #return
    #r = json.load(request.body)
    name = request.forms.get('name')
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    #Check if any details are 
    if name and username and password:
        res = functions.addUser(name, username, password)
    else:
        return{"status": 401, "success": False, "message": "One of the fields is empty. Please use non empty values."}
    
    #Check if user was stored in db successfully.
    if res['success'] == True:
        return {"status": 200, "success": True, "data": {"user_id": res['user_id']}}
    else:
        return {"status": 401, "success": False, "message": res['message']}

###
#
#   Login - Retrieves user's username and password and checks for user in DB
#   Input - username, password
#   Response - 200, success, user_id
#
# Registration
# To Test Use:
#   curl -X POST -H "Content-Type: application/json" -d '{"username":"xxxx","password":"xxxx"}' http://localhost:8080/v1/login

@post('/v1/login')
def login():
    #r = json.load(request.body)
    username = request.forms.get('username')
    password = request.forms.get('password')
    res = functions.loginUser(username, password)
    if res['success'] == True:
        return {"status": 200, "success": True, "data": {"user_id": res["user_id"]}}
    else:
        return {"status": 401, "success": False, "message" : res["message"]}


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
    res = functions.getUser(user_id)
    #print data
    
    if res["success"]:
        user = res['user']
        return {"status": 200, "success": True, "data": user}
    else:
        return {"status": 401, "success": False, "message": res['message']}

###
#
#   Add Board - Creates a new board in the DB
#   Input - boardName, 
#   Response - 200, success, boardID
#
###
@post('/v1/user/<user_id>/board')
def add_board(user_id):
    #r = json.load(request.body)
    board_name = request.forms.get('board_name')
    board_id = functions.addBoard(board_name)
    update = functions.updateUser(user_id, board_id)
    if update['success']:
        return {"status": 200, "success": True, "data": board_id}

###
#
#   Get Board - Get board from the DB
#   Input -  
#   Response - 200, success, board {boardName, pins[]}
#
###
@get('/v1/boards/<board_id>')
def get_board(board_id):
    return functions.getBoard(board_id)

###
#
#   Delete Board - Delete board from the DB
#   Input -  
#   Response - 200, success, board {boardName, pins[]}
#
###
@delete('/v1/user/<user_id>/board/<board_id>')
def delete_board(user_id,board_id):
    return functions.deleteBoard(user_id, board_id)
    
###
#
#   Add Comment - Get board from the DB
#   Input -  
#   Response - 200, success, board {boardName, pins[]}
#
###
@post('/v1/user/<user_id>/pin/<pin_id>/comment')
def add_comment(user_id, pin_id):
    comment = request.forms.get('comment')
    functions.addComment(user_id, pin_id, comment)
    return "Added Comment"


# To Upload Using Curl
# curl --form upload=@localfilename --form press=OK [URL] 
@post('/v1/user/<user_id>/pin')
def upload(user_id):
    pin_name = request.forms.get('pin_name')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'

    save_path = "./pins"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    res = functions.createPin(pin_name, save_path)
    pin_file_name = "pinimage:"+str(res['pin_id'])
    file_path = "{path}/{file}".format(path=save_path, file=pin_file_name)
    upload.save(file_path)
    return "File successfully saved to '{0}'.".format(save_path)
    

# To attach an existing pin to a user on a board
@post('/v1/user/<user_id>/board/<board_id>')
def attach_pin(user_id, board_id):
    pin_id = request.forms.get('pin_id')
    functions.attachPin(board_id,pin_id)
    return


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
    return functions.getAllPins()

###
#
#   Get a Pin - Get a Pin from the DB
#   Input -  pin_id
#   Response - 200, success, pin {pin_name, pin_url, comments[{ user, comment }]}
#

@get('/v1/pin/<pin_id>')
def get_pin(pin_id):
    return functions.getPin(pin_id)
    
###
#
#   Get All Boards - Returns all available Boards from DB
#   Input -
#   Response - 200, success, boards[]
#

@get('/v1/boards')
def get_all_boards():
    return json.dumps(functions.getAllBoards())
    #Retrieves pin name and enters it into DB
    #????? How are we going to do the upload image part ?????
    #get pinID from newly created pin
    #return response
    
run(host='localhost', port=8080, debug=True)