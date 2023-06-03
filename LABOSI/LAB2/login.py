
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Hash import SHA256
from getpass import getpass

import sys
import pickle
import os.path


def load():
    dic = {}
    if os.path.isfile('sifre.bin'):
        file = open('sifre.bin', 'rb')
        dic = pickle.load(file)
        file.close()
    
    return dic

def provjeriLozinku(username, lozinka):
    dic = load()
    if username in dic:
        info = dic[username]
        salt = info["salt"]
        pravaLozinka = info["pass"]
        upisanaLozinka = scrypt(lozinka.encode("UTF-8"), salt, 16, N=2**14, r=8, p=1)
        if (upisanaLozinka == pravaLozinka):
            if (info["flag"] == "true"):
                a = promjeniPass(dic, username)
                if (a == True):
                    print("Login successful.")
            else:
                print("Login successful.")
            return 0
        else:
            return 1
            
    else:
        return 1
            
def promjeniPass(dic, username):
    lozinka = getpass("New Password:")
    ponoviLozinku = getpass("Repeat Password:")
    if (lozinka == ponoviLozinku):
        salt = get_random_bytes(16)  #generiramo salt za novog usera
        lozinkaHash = scrypt(lozinka.encode("UTF-8"), salt, 16, N=2**14, r=8, p=1)
        userinfo =  {"salt": salt, "pass": lozinkaHash, "flag": "false"}
        dicDva={}
        for key in dic:
            if (key!=username):
                dicDva[key] = dic[key]
            else:
                dicDva[key] = userinfo
        file = open('sifre.bin', 'wb')
        pickle.dump(dicDva, file)
        file.close()
        return True

    else:
        print("Password mismatch, please try again")
        return False
    

if __name__ == "__main__":
    n = len(sys.argv)

    if (n < 2):
        print("nedovoljno argumenata")
    else:
        username = sys.argv[1]
        brojLoginova = 0
        
        while (brojLoginova < 3):
            lozinka = getpass("Password:")
            a = provjeriLozinku(username, lozinka)
            if (a == 0):
                break
            brojLoginova = brojLoginova + a
            print("Username or password incorrect.")
