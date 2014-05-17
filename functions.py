import fdb
import json

# Connection to Datbase
fdb.api_version(200)
db = fdb.open()

# Global Variables
next_uid = 1
next_board_id = 1
next_pin_id = 1

# Setup initial values for next ids of users, boards and pins
def setup():
    global next_uid
    global next_board_id
    global next_pin_id
    while db["users:"+str(next_uid)]:
        next_uid+=1
    while db["boards:"+str(next_board_id)]:
        next_board_id+=1
    while db["pins:"+str(next_pin_id)]:
        next_pin_id+=1
    return

def addUser(n, un, p):
    global next_uid
    user_id = next_uid
    next_uid += 1
    name = n
    username = un
    password = p
    print db['username:'+str(un)]
    if db['username:'+str(un)]:
        return {"success": False, "message": "Existing Username. Choose a different username"}
    user = {"name": name, "username": username, "password": password, "boards": []}
    value = json.dumps(user)
    key = "users:"+str(user_id)
    print key + ' ---> ' + value
    db["username:"+str(username)] = str(user_id)
    db[key] = value
    return {"success": True, "user_id": user_id}

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
    if checkUser(uid):
        get_user = db['users:'+str(uid)]
        u = json.loads(get_user)
        #print str(u)
        return {"success": True, "user": u}
    else:
        return {"success": False, "message": "User not found"}
    
def updateUser(uid, bid):
    if not checkUser(uid):
        return {"success": False, "message": "User not found"}
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
    return {"success": True}
    
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

def getBoard(bid):
    boards = db.get_range_startswith("boards:", reverse=True)
    for i in range(0,len(boards)):
        key = boards[i].key
        if key == ("boards:"+bid):
            found_board = boards[i].value
            print json.dumps(found_board)
            return json.dumps(found_board)
    return {"success": False, "message": "No board found"}

def getPin(bid):
    pins = db.get_range_startswith("pins:", reverse=True)
    for i in range(0,len(pins)):
        key = pins[i].key
        if key == ("pins:"+bid):
            found_pin = pins[i].value
            print json.dumps(found_pin)
            return json.dumps(found_pin)
    return {"success": False, "message": "No pin found"}

def getAllBoards():
    tmp = []
    boards = db.get_range_startswith("boards:", reverse=True)
    for i in range(0,len(boards)):
        key = boards[i].key
        value = boards[i].value
        j = { key : json.loads(value) }
        tmp.append(j)
    #print tmp
    return tmp

def deleteBoard(uid,bid):
    #del db["boards:"+str(bid)]
    user = json.loads(db["users:"+uid])
    boards = user['boards']
    new_boards_list = []
    #print json.dumps(boards)
    print (bid in boards)
    for i in range(0, len(boards)):
        if bid != boards[i]:
            new_boards_list.append(boards[i])
    user["boards"] = new_boards_list
    db["users:"+str(uid)] = json.dumps(user)
    print json.dumps(user)
    return {"success": True, "message": "Board deleted"}

def createPin(pn, path):
    global next_pin_id
    pin_id = next_pin_id
    next_pin_id += 1
    pin_name = pn
    pin_url = path+str(next_pin_id)
    pin = {"pin_id": pin_id, "pin_name": pin_name, "pin_url": path, "comments":[]}
    key = "pins:"+str(pin_id)
    value = json.dumps(pin)
    db[key] = value
    return {"pin_id": pin_id, "pin_name": pin_name}
    #return pin_id

def attachPin(bid, pid):
    if not db["boards:"+bid]:
        return {"success": False, "message":"Invalid Board Id"}
    if not db["pins:"+pid]:
        return {"success": False, "message":"Invalid Pin Id"}
    b = db['boards:'+str(bid)]
    board = json.loads(b)
    pins = board['pins']
    print pins
    pins.append(pid)
    board['pins'] = pins
    print pins
    print b
    b = json.dumps(board)
    key = "boards:"+str(bid)
    db[key] = b
    return {"success": True, "message":"Attached Pin"+pid+ " to Board "+"bid"}

def getAllPins():
    tmp = []
    pins = db.get_range_startswith("pins:", reverse=True)
    for i in range(0,len(pins)):
        key = pins[i].key
        value = pins[i].value
        j = { key : json.loads(value) }
        tmp.append(j)
    return json.dumps(tmp)

def addComment(uid,pid,comment):
    pin = json.loads(db['pins:'+str(pid)])
    user = json.loads(db["users:"+uid])
    user_name = user['username']
    comments = pin['comments']
    new_comment = {"user": user_name, "comment": comment}
    comments.append(new_comment)
    pin['comments'] = comments
    db["pins:"+str(pid)] = json.dumps(pin)
    print json.dumps(comments)

if __name__ == "__main__":
    main()