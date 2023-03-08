#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import fileinput
import hashlib

BASIS = "Dokumentation"

aenderung = False

def neuer(quelle, compiliert):
	return (not os.path.isfile(compiliert)) or os.path.getmtime(quelle) > os.path.getmtime(compiliert)

def runcommand(command):
	print command
	os.system(command)

def inkscape(datei,pdf):
	runcommand("inkscape " + datei + " --export-pdf " + pdf )

def inkscape_tex(datei,pdf):
	runcommand("inkscape " + datei + " --export-latex --export-pdf " + pdf )

def get_hash(datei):
	if os.path.isfile(datei):
		return hashlib.md5(open(datei).read()).hexdigest()
	else:
		return 0

def get_auxloghash(NAME):
	return get_hash(NAME + ".aux") + get_hash(NAME + ".log")

if neuer("ligatures.map", "ligatures.tec"):
	runcommand("teckit_compile ligatures.map")

for datei in os.listdir(os.getcwd()):
	if datei.endswith(".svg"):
		pdf = datei[:-4] + ".pdf"
		if neuer(datei, pdf):
			if datei.endswith("_tex.svg"):
				inkscape_tex(datei,pdf)
			else:
				inkscape(datei,pdf)
			aenderung = True

for sprache in [(1,"de"), (2,"en")]:
	for schrift in [(1,"fraktur"), (2,"antiqua")]:
		
		NAME = BASIS + "_" + sprache[1] + "_" + schrift[1]
		
		if neuer(BASIS + ".tex", NAME + ".pdf"):
			aenderung = True
		
		while aenderung:
			auxloghash = get_auxloghash(NAME)
			
			runcommand("xelatex"
				+ " -jobname=" + NAME
				+ " -interaction=nonstopmode"
				+ " '"
				+ "\\newcommand{\\DTEN}[2]{#%i}" % sprache[0]
				+ "\\newcommand{\\fraq}[2]{#%i}" % schrift[0]
				+ "\\input{Dokumentation.tex}"
				+ "'")
			
			aenderung = (auxloghash != get_auxloghash(NAME))


