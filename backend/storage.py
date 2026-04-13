import json

def save_data(tasks):
    """save data to json"""
    with open("tasks.json", "w") as file: #opens new json file in write mode named as file
        json.dump(tasks, file, indent=4) #dump will take the data and write into json 

def load_data():
    """load data from json"""
    try:
        with open ("tasks.json", "r") as file: #will open json file by name in read mode
            return json.load(file) #will return data from json file
    except FileNotFoundError: #if file does not exist, load empty list
        return []
    
def save_user_prof(username, hpassword):
    data = {
        "username":username,
        "hpassword":hpassword.hex()
    } 
    with open("user_prof.json", "w") as file:
        json.dump(data, file, indent=4)

def load_user_prof():
    try:
        with open("user_prof.json", "r") as file:
            data = json.load(file)
            data['hpassword'] = bytes.fromhex(data['hpassword'])
            return data
    except FileNotFoundError:
        return None
