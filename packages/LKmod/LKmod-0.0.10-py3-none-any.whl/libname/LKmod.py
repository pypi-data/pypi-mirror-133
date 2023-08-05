lock="NaN"
key="NaN"
checkl=" "
checkk=" "
def check_lock():
    global checkl
    if lock=="True":
        print("lock on")
        checkl=1
    elif lock=="False":
        print("lock off")
        checkl=0
    return checkl
        
def check_key():
    global checkk
    if key=="True":
        print("key on")
        checkk=1
    elif key=="False":
        print("key off")
        checkk=0
    return checkk
