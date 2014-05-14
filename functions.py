import fdb
import json

# Connection to Datbase
fdb.api_version(200)
db = fdb.open()

# Global Variables
next_uid = 1
next_board_id = 1
next_pin_id = 1

def addUser(n, un, p):
    global next_uid
    user_id = next_uid
    next_uid += 1
    name = n
    username = un
    password = p
    user = {"name": name, "username": username, "password": password, "boards": []}
    value = json.dumps(user)
    key = "users:"+str(user_id)
    print key + value
    db["username:"+str(username)] = str(user_id)
    db[key] = value
    return user_id

def loginUser(un, p):
    username = un
    password = p
    user_id = db['username:'+str(username)]
    user = db['users:'+str(user_id)]
    user = json.loads(user)
    if password == user['password']:
        return {"success": True, "user_id": user_id}
    else:
        return {"success": False, "message": "invalid user"}

def getUser(uid):
    get_user = db['users:'+str(uid)]
    u = json.loads(get_user)
    print u['name']
    return u
    
def updateUser(uid, bid):
    u = db['users:'+str(uid)]
    user = json.loads(u)
    boards = user['boards']
    print boards
    boards.append(bid)
    user['boards'] = boards
    u = json.dumps(user)
    key = "users:"+str(uid)
    print boards
    print u
    db[key] = u
    return True
    
def checkUser(uid):
    if db["users:"+str(uid)]:
        return True
    else:
        return False
    
def addBoard(n):
    global next_board_id
    board_id = next_board_id
    next_board_id += 1
    board_name = n
    board = {"board_name": board_name, "pins": []}
    value = json.dumps(board)
    key = "boards:"+str(board_id)
    print key + value
    db[key] = value
    return board_id
    
def postPin(pid, bid):
    b = db['boards:'+str(bid)]
    board = json.loads(b)
    pins = board['pins']
    print pins
    pins.append(pid)
    board['pins'] = pins
    b = json.dumps(board)
    key = "boards:"+str(bid)
    print pins
    print b
    db[key] = b
    return board
    
    
if __name__ == "__main__":
    main()