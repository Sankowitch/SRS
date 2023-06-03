#!/bin/bash
chmod +x usermgmt
chmod +x login
echo "SADA RADI PROGRAM USERMGMT"
echo "PRIMJER1: Upisite dvije razlicite lozinke, sada se radi dodavanje korisnika kiki"
python3 usermgmt add kiki
echo "PRIMJER2: Upisite dvije iste lozinke, sada se radi dodavanje korisnika kiki"
python3 usermgmt add kiki
echo "PRIMJER3: dodavanje jos jednog korisnika hulio, upisite 2 iste lozinke"
python3 usermgmt add hulio
echo "PRIMJER4: dodavanje jos jednog korisnika vincent77, upisite 2 iste lozinke"
python3 usermgmt add vincent77
echo "PRIMJER5: sada se radi brisanje korisnika dobarDabar - koji nije prethodno dodan"
python3 usermgmt del dobarDabar
echo "PRIMJER6: sada se radi brisanje korisnika vincent77"
python3 usermgmt del vincent77
echo "PRIMJER7: sada se radi promjena lozinke za vincent77, kojeg nema u bazi- provjera jeli naredba delete radi"
python3 usermgmt passwd vincent77
echo "PRIMJER8: sada se radi promjena lozinke za kiki"
python3 usermgmt passwd kiki
echo "PRIMJER9: sada se radi dizanje zastavice za forsiranje promjene lozinke za kiki"
python3 usermgmt forcepass kiki
echo "SADA RADI PROGRAM LOGIN"
echo "PRIMJER10: upisivanje korisnika vincent77 kao login-korisnik ciji username ne postoji ili je kriv- u ovom slucaju ne postoji jer je prethodno izbrisan iz baze"
python3 login vincent77
echo "PRIMJER11: upisivanje korisnika koji postoji- hulio, ali krive sifre (upisite krivu lozinku- SVA TRI PUTA)"
python3 login hulio
echo "PRIMJER12: upisivanje korisnika koji postoji- hulio, ali dobru lozinku (UPISITE 1. 2. ILI 3. PUT DOBRU LOZINKU)"
python3 login hulio
echo "PRIMJER13: upisivanje korisnika koji ima dignutu zastavicu za forcepass - kiki, ali upisivanje STARE sifre kao NOVE SIFRE (pod new pass upisite istu stvar kao i za password)"
python3 login kiki
echo "PRIMJER14: upisivanje korisnika koji ima dignutu zastavicu za forcepass - kiki, ali upisivanje nove sifre pod new pass"
python3 login kiki
echo "PRIMJER15: upisivanje korisnika koji je imao dignutu zastavicu za forcepass - kiki, te sad upisuje novu lozinku"
python3 login kiki
