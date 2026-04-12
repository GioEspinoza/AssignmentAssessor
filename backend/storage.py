import json
def save_data(tasks):
    """save data to json"""
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

def load_data():
    """load data from json"""
    try:
        with open ("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_profile(username, hpassword):
    data = {
        "username":username,
        "hpassword":hpassword
    } 
    with open("user_prof.json", "w") as file:
        json.dump(data, file, indent=4)

def load_user_prof():
    try:
        with open("user_prof.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None