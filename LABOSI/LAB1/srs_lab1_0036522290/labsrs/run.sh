#!/bin/bash
python3 tajnik.py init nekimasterpass
python3 tajnik.py put nekimasterpass akaunt1 sifra1
python3 tajnik.py get nekimasterpass akaunt1
python3 tajnik.py put nekimasterpass akaunt2 sifra2
python3 tajnik.py put nekimasterpass akaunt3 sifra3
python3 tajnik.py put nekimasterpass akaunt1 SIFRA1
python3 tajnik.py get nekimasterpass akaunt1
python3 tajnik.py get nekimasterpass akaunt4
python3 tajnik.py put krivimasterpass akaunt3 sifra3
python3 tajnik.py get KRIVImasterpass akaunt1
