import os
import hashlib #python hash, pbkdf2_hmac does password hashes
#####################################################################################

### 3 jobs are done in hash_password, including the making of the random salt, 
### then hashing the password using the salt, 
### and then returinng the final output of both salt and hash together

#hashing are chain based aglorithms that depend on the last step to hash the next.
#a salt is used to change the first input before hashing ensuring all password hashes are different

def hash_password(password): #takes the plain password from the user to convert to hash

    salt = os.urandom(16) #Generates 16 random bytes for salt that are cryptographically secure. W/o salt rainbow tables break through

    key = hashlib.pbkdf2_hmac( #starts password hash, key will hold final hash

        'sha256', #hash algorithm in use, layered with pbkdf2

        password.encode(), #converts password string to bytes using standard encoding, hash function can only work on bytes

        salt, #gives function the salt to combine with hash key

        100000 # number of iterations, will hash x amount of times
    )
    return salt + key #return both salt and key together, original salt is needed for verification
    # output: first 16 bytes - og salt, remaining bytes will be acutal hash key


def check_hpassword(hpassword, attempt): #will check password attempt
    salt = hpassword[:16] #will get salt by taking first 16 letters from stored hpassword
    stored_key = hpassword[16:] #rest must be the hash password

    #using the stored salt, it will replicate the hashing process to validate
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        attempt.encode(),
        salt,
        100000
    )

    return new_key == stored_key #compare to see if hashing results are equal.

######################################################################################

# ensuring name is not empty, no numbers, and no double spaces. Looping if name isnt valid, welcoming if it is valid.
def check_new_name(name):
    user = name.strip()
    if not user or any(char.isdigit() for char in user) or "  " in user:
        return False, "Not valid name! Please try again"
    return True, ""

#ensures new password meets criteria
def check_new_pass(password):
    if not password or len(password) < 8 or "  " in password:
        return False, "Not valid password! Please try again"
    return True, "Valid password"