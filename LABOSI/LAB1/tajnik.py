
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

import sys


def initialisation(masterpass):
    file = open('sifre.bin','wb') 
    salt = get_random_bytes(16)  #getanje salta
    
    hash_object = SHA256.new(masterpass.encode("UTF-8"))

    #kljucevi
    keys = PBKDF2( masterpass, salt, 64, count=1000000, hmac_hash_module=SHA512)
    key = keys[:32]
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
 
    
    #print(salt.length)
    #print(nonce.length)
    
    ciphertext, tag = cipher.encrypt_and_digest(hash_object.digest())
    
    file.write(salt)
    file.write(tag)
    file.write(nonce)
    file.write(ciphertext)

    file.close()
    print("Password manager initialized.")
    return 




def checkMasterpass(masterpass, adresa, sifra, provjera):
    hash_object = SHA256.new(masterpass.encode("UTF-8"))
    file = open('sifre.bin','rb')
    
    salt = file.read(16)
    tag = file.read(16)
    nonce = file.read(16)
   
    sve = file.read(-1)
    
    file.close()

    spremljeniHash=""
    keys = PBKDF2( masterpass, salt, 64, count=1000000, hmac_hash_module=SHA512)
    key = keys[:32]

    #dohvati hash od mastera koji je zapisan
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)


    try:
        sveDekriprt = cipher.decrypt_and_verify(sve, tag)
        spremljeniHash = sveDekriprt[0:32]
        ostatakTeksta = sveDekriprt[32:]

    except(ValueError, KeyError):
        print("Master password incorrect or integrity check failed. ")
    
    if (hash_object.digest() == spremljeniHash):
        #print("YAS")
        if (provjera == "put"):
            stavi(masterpass, adresa, sifra, spremljeniHash, ostatakTeksta)
        if (provjera == "get"):
            vratiPassZaAdresu(ostatakTeksta, adresa, True)
    else:
        #print("Master password incorrect or integrity check failed. ")
        return False
    
    return True

def stavi(masterpass, adresa, sifra, hashb, ostatakBajtova):
    a = "Stored"
    imaLiVecTaAdresa = vratiPassZaAdresu(ostatakBajtova, adresa, False)
    if (imaLiVecTaAdresa[0] >= 0):
        moj_string = ostatakBajtova.decode("UTF-8")
        moj_string = moj_string.replace(imaLiVecTaAdresa[1], "")
        ostatakBajtova = moj_string.encode("UTF-8")
        a="Updated"

        
    
        
    
    salt = get_random_bytes(16)
    keys = PBKDF2( masterpass, salt, 64, count=1000000, hmac_hash_module=SHA512)
    key = keys[:32]

    parAdresaSifra = adresa + " " + sifra + " "
    parAdresaSifraB = parAdresaSifra.encode("UTF-8")
    ostatakBajtova= ostatakBajtova + parAdresaSifraB
    
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(hashb + ostatakBajtova) 

    file = open('sifre.bin','wb')

    file.write(salt)
    file.write(nonce)
    file.write(tag)
    file.write(ciphertext)

    file.close()

    print("{} password for {}.".format(a, adresa))


    return


def vratiPassZaAdresu(tekst, adresa, printaj):
    #print(tekst.decode("UTF-8"))
    moj_string = tekst.decode("UTF-8")
    imaLiAdrese = moj_string.find(adresa)
    sifra=""
    if (imaLiAdrese >= 0):
        sifra=""
        pocetak = imaLiAdrese + len(adresa) + 1 #pocetak sifre
        for i in range(pocetak, len(moj_string)):
            if (moj_string[i] == " "):
                break
            sifra = sifra + moj_string[i]
        if (printaj == True):
            print("Password for {0} is: {1}.".format(adresa, sifra))
    else:
        if (printaj == True):
            print("No password saved for the given address.")
       
        
    return (imaLiAdrese, adresa + " " + sifra + " ")



if __name__ == "__main__":
    n = len(sys.argv)
    #inicijalizacija alata i stvaranje prazne baze podataka
    init = "init"
    put = "put"
    get = "get"
    
    inicijalizirali = False
    masterSifra=""


    #ucitavanje iz retka narebe za program
    if (n < 3):
        print("nedovoljno argumenata")
    for i in range(1, n):
        #inicijalizacija
        if (sys.argv[i] == init):
            inicijalizirali = True
            masterSifra = sys.argv[i+1]
            initialisation(masterSifra)

        #stavljanje sifre i adrese
        if (sys.argv[i] == put):
            masterSifra = sys.argv[i+1]
            adresa = sys.argv[i+2]
            sifra = sys.argv[i+3]
            uspjeliPuttati = checkMasterpass(masterSifra, adresa, sifra, put)
            
        #gettanje sifre od dane adrese
        if (sys.argv[i] == get):
            masterSifra = sys.argv[i+1]
            adresa = sys.argv[i+2]
            uspjeliGettati = checkMasterpass(masterSifra, adresa, None , get)


       
            