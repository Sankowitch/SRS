
from numpy import ScalarType, byte
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Hash import SHA256
from getpass import getpass
import os.path

import sys
import pickle


def dodaj(username, lozinka, zastavica) :
    salt = get_random_bytes(16)  #generiramo salt za novog usera
    lozinkaHash = scrypt(lozinka.encode("UTF-8"), salt, 16, N=2**14, r=8, p=1)
    
    newUser = {"salt": salt, "pass": lozinkaHash, "flag": zastavica}

    dicOfUsers = {}
    dicOfUsers[username] = newUser

    dicDva = load()
    if (len(dicDva) > 0):
        for key  in dicDva:
            dicOfUsers[key]= dicDva[key]

    file = open('sifre.bin', 'wb')
    pickle.dump(dicOfUsers, file)
    file.close()

def naredbe(username, brisi, digniZastavicu, noviPass, lozinka):   #returna info o useru kojega mice
    dic = load() 
    dicDva = {}
    userinfo = {}

    if username in dic:
        for key in dic:
            if (key != username):
                dicDva[key] = dic[key]
            else: 
                userinfo = dic[key]
                if (digniZastavicu == True):   #ako je digni zastaviuu true dinut ce je
                    userinfo["flag"] = "true"
                if (noviPass == True):         #ako mijenjamo loziku generiramo novi salt
                    salt = get_random_bytes(16)  #generiramo salt za novog usera
                    lozinkaHash = scrypt(lozinka.encode("UTF-8"), salt, 16, N=2**14, r=8, p=1)
                    userinfo["salt"] = salt
                    userinfo["pass"] = lozinkaHash
                if (brisi == False):         #ako imamo novu sifru ili dizemo sastavicu funckija nece biti u mode-u brisi
                    dicDva[key] = userinfo
        
        file = open('sifre.bin', 'wb')
        pickle.dump(dicDva, file)
        file.close()
        
    else:
        print("There is no user {} in database".format(username))
        
    return userinfo


def load():
    dic = {}
    if os.path.isfile('sifre.bin'):
        file = open('sifre.bin', 'rb')
        dic = pickle.load(file)
        file.close()
    
    return dic

def ispisi():
    dbfile = open('sifre.bin', 'rb')     
    db = pickle.load(dbfile)
    for keys in db:
        print(keys, '=>', db[keys])
        
    dbfile.close()

    





if __name__ == "__main__":
    n = len(sys.argv)

    add = "add"
    passwd ="passwd"
    forcepass ="forcepass"
    delete = "del"
    printaj = "p"


    if (n < 3):
        print("nedovoljno argumenata")
    else:
        username = sys.argv[2]
        naredba = sys.argv[1]

        if (naredba == add):
            lozinka = getpass("Password:")
            ponoviLozinku = getpass("Repeat Password:")
            if (lozinka == ponoviLozinku ):
                dodaj(username, lozinka, "false")
                print("User {} succesfuly added".format(username))
            else:
                print("User add failed. Password mismatch.")
        
        if (naredba == delete):
            #naredbe funckija prima (username, brisanje, dizanjeZastavice, promjenaLozinke, lozinka)
            uspjelo = naredbe(username, True, False, False, lozinka ="" )
            if (len(uspjelo) > 0):
                print("User succesfuly removed")
        if (naredba == printaj):
            ispisi()
        
        if (naredba == passwd):
            lozinka = getpass("Password:")
            ponoviLozinku = getpass("Repeat Password:")   
            if (lozinka == ponoviLozinku):
                
                uspjelo = naredbe(username, False, False, True, lozinka)
                if (len(uspjelo) > 0):
                    print("Password change successful.")
                
            else:
                print("Password change failed. Password mismatch.")
        
        if (naredba == forcepass):
            uspjelo = naredbe(username,False, True, False, "")
            if (len(uspjelo) > 0):
                print("User will be requested to change password on next login.")

            


         
            