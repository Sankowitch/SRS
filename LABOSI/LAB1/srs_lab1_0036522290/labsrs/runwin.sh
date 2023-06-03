#!/bin/bash
python tajnik.py init nekimasterpass
python tajnik.py put nekimasterpass akaunt1 sifra1
python tajnik.py get nekimasterpass akaunt1
python tajnik.py put nekimasterpass akaunt2 sifra2
python tajnik.py put nekimasterpass akaunt3 sifra3
python tajnik.py put nekimasterpass akaunt1 SIFRA1
python tajnik.py get nekimasterpass akaunt1
python tajnik.py get nekimasterpass akaunt4
python tajnik.py put krivimasterpass akaunt3 sifra3
python tajnik.py get KRIVImasterpass akaunt1