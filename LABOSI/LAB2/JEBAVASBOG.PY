
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Hash import SHA256
from getpass import getpass

import sys


def dodaj(username, lozinka, force):
    #dodajemo 
    salt = get_random_bytes(16)  #generiramo salt za novog usera
    lozinkaHash = scrypt(lozinka.encode("UTF-8"), salt, 16, N=2**14, r=8, p=1)


    changeP = "forcepassChange:false"
    if (force == True):
        changeP = "forcepassChange:true"
    
    string =username + " " + str(salt) + " " + str(lozinkaHash) + " "+ changeP + "\n"  #odvojeni razmakom jer je to ascii 32
    
    print(str(salt))
    print(salt.decode("ASCII"))

    print()

    file = open('sifre.txt', 'a') 
    file.write(string)
    #file.write("\n")
    file.close()

    

def promjeniLozinku(username, lozinka):

    changeP = izbrisiKorisnika(username)
    if (changeP == -1):   #tog korisnka nije bilo
        return
    
    if (changeP.find(" forcepassChange:true") != -1):
        dodaj(username, lozinka, True)
    else:
        dodaj(username, lozinka, False)

    print("Password change successful.")
    
   
    
def izbrisiKorisnika(username):
    file = open('sifre.txt','r')
    lines = file.readlines()
    file.close()

    changeP= ""
    
    index = 0
    indexToSkip = -1
    
    for line in lines:
        polje = line.split(" ")
        if ( polje[0] == username):
            changeP = line 
            indexToSkip = index
            break
        index = index + 1

    if (indexToSkip == -1):
        print("There is no user {} in database. ".format(username))
        return indexToSkip

    index = 0
    file = open('sifre.txt','w')
    for line in lines:
        if (index  != indexToSkip):
            file.write(line)
        
        index = index + 1
    file.close()

    return changeP

def promjeniLozinkuUser(username):
    returnIz = izbrisiKorisnika(username)

    if (returnIz == -1):
        return
 
    polje = returnIz.split(" ")
    string = polje[0] + " " + polje[1] + " " + polje[2] + " " + "forcepassChange:true" + "\n"
    file = open('sifre.txt', 'a') 
    file.write(string)
    #file.write("\n")
    file.close()
    print("User will be requested to change password on next login.")
    
            






if __name__ == "__main__":
    n = len(sys.argv)

    add = "add"
    passwd ="passwd"
    forcepass ="forcepass"
    delete = "del"


    if (n < 3):
        print("nedovoljno argumenata")
    else:
        username = sys.argv[2]
        naredba = sys.argv[1]

        if (naredba == add):
            lozinka = getpass("Password:")
            ponoviLozinku = getpass("Repeat Password:")
            a = False
            if (lozinka.find(" ") > -1):
                print("Password can't contain space.")
                a = True
            if (lozinka == ponoviLozinku and a == False):
                dodaj(username, lozinka, False)
                print("User {} successfuly added.".format(username))
            else:
                print("User add failed. Password mismatch.")
        if (naredba == passwd):
            lozinka = getpass("Password: ")
            ponoviLozinku = getpass("Repeat Password: ")
            if (lozinka == ponoviLozinku):
                promjeniLozinku(username, lozinka)
            else: 
                print("Password change failed. Password mismatch.")
        if (naredba == delete):
            a = izbrisiKorisnika(username)
            if (a != -1):
                print("User successfuly removed.")
        if (naredba == forcepass):
            promjeniLozinkuUser(username)
            