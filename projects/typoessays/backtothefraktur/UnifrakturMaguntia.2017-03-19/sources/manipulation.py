#! /usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput
import os
import subprocess
import shutil
import ast

def string_auswerten(string):
	try:
		string = ast.literal_eval(string)
	except ValueError:
		pass
	return string

def datei_nach_glyph(dateiname):
	chars = list(dateiname[:-6])
	i = 0 
	while i < len(chars):
		if (chars[i]=="_") and chars[i+1].isupper():
			chars.pop(i)
		i+=1
	return "".join(chars)

def glyph_nach_datei(glyph):
	if glyph.startswith("uni"):
		return glyph + ".glyph"
	else:
		chars = list(glyph)
		i = 0
		while i < len(chars):
			if chars[i].isupper():
				chars.insert(i, "_")
				i+=1
			i+=1
		return "".join(chars) + ".glyph"

def stems_zerlegen(stemstring):
	ausgabe = []
	for stem in stemstring.split(">"):
		if stem.strip():
			ebene = stem.split("<")[0].split()
			positionen_roh = stem.split("<")[1].split()
			positionen = map(list,zip(*[iter(positionen_roh)]*2))
			ausgabe += [[ebene, positionen]]
	return ausgabe

def stems_vereinen(stemslist):
	ausgabe = []
	for stem in [stem for stems in stemslist for stem in stems]:
		neu = True
		for bestehender_stem in ausgabe:
			if stem[0] == bestehender_stem[0]:
				bestehender_stem[1] += stem[1]
				neu = False
				break
		if neu:
			ausgabe += [stem]
	return ausgabe

def stems_nach_string(stems):
	ausgabe = ""
	for stem in stems:
		ausgabe += " ".join(stem[0])
		ausgabe += "<"
		ausgabe += " ".join([komp for position in stem[1] for komp in position])
		ausgabe += "> "
	return ausgabe

class Schrift:
	def __init__(self, name, quellordner):
		self.name = name
		self.ordner = self.name + ".sfdir"
		if self.ordner in os.listdir("."):
			raise Exception("Fehler: Zielordner existiert bereits.")
			return None 
		else:
			os.mkdir(self.ordner)
		
		self.props = []
		
		for datei in os.listdir(quellordner):
			if os.path.isfile(quellordner + "/" + datei):
				shutil.copy(quellordner + "/" + datei, self.ordner)
		
		self.props_oeffnen()
		for i,zeile in enumerate(self.props):
			for nameString in ["FontName:", "FullName:", "FamilyName:"]:
				if zeile.startswith(nameString):
					self.props[i] = nameString + " " + self.name + "\n"
	
	def __del__(self):
		self.props_schliessen()
	
	def props_oeffnen(self):
		if not self.props:
			with open(self.ordner + "/font.props", "r") as propsdatei:
				self.props = propsdatei.readlines()
	
	def props_schliessen(self):
		if self.props:
			with open(self.ordner + "/font.props", "w") as propsdatei:
				propsdatei.writelines(self.props)

	def in_kerns_ersetzen(self, quelle, ziel=""):
		self.props_oeffnen()
		in_kerningtabelle = True
		for i,zeile in enumerate(self.props):
			if zeile.startswith("KernClass2"):
				in_kerningtabelle = True
				anzahl_vor = zeile.split()[1]
			elif in_kerningtabelle:
				if zeile.startswith(" ") and not ("{}" in zeile):
					inhalt = zeile.split()[1:]
					if quelle in inhalt:
						if ziel == "":
							inhalt.remove(quelle)
						else:
							inhalt[inhalt.index(quelle)] = ziel
					neuer_inhalt = " ".join(inhalt)
					self.props[i] = " " + str(len(neuer_inhalt)) + " " + neuer_inhalt + "\n"
				else:
					in_kerningtabelle = False

	def aus_subs_entfernen(self, ziel):
		self.props_oeffnen()
		in_sub = True
		for i,zeile in enumerate(self.props):
			if zeile.startswith("ChainSub2"):
				in_sub = True
				in_kerningtabelle = False
			elif in_sub:
				if zeile.startswith("  BClass:") or zeile.startswith("  FClass:"):
					zeile_zerl = zeile.split()
					header = zeile_zerl[0]
					inhalt = zeile_zerl[2:]
					if ziel in inhalt:
						inhalt.remove(ziel)
					neuer_inhalt = " ".join(inhalt)
					self.props[i] = "  " + header + " " + str(len(neuer_inhalt)) + " " + neuer_inhalt + "\n"
				elif zeile[:2] != "  ":
					in_sub = False
	
	def ersetzen (self, ziel, quelle, name_uebernehmen=True):
		zieldatei = glyph_nach_datei(ziel)
		quelldatei = glyph_nach_datei(quelle)
		
		self.in_kerns_ersetzen(ziel)
		if name_uebernehmen:
			self.aus_subs_entfernen(quelle)
			self.in_kerns_ersetzen(quelle, ziel)
		else:
			self.aus_subs_entfernen(ziel)
		
		for zeile in open(self.ordner + "/" + zieldatei, "r"):
			if zeile.startswith("Encoding:"):
				Encoding = zeile
		
		if name_uebernehmen:
			shutil.move(self.ordner + "/" + quelldatei, self.ordner + "/" + zieldatei)
		else:
			os.remove(self.ordner + "/" + zieldatei)
			zieldatei = quelldatei
		
		for zeile in fileinput.input (self.ordner + "/" + zieldatei, inplace=1):
			if zeile.startswith("Encoding:"):
				altes_Encoding = zeile
				print Encoding,
			elif zeile.startswith("StartChar:") and name_uebernehmen:
				print "StartChar: " + ziel
			else:
				print zeile,
		
		try:
			#for datei in os.listdir(self.ordner):
			for datei in subprocess.check_output([
					"grep -l \"Refer: " + altes_Encoding.split()[3] + " \" " + self.ordner + "/*.glyph"
				], shell=True).split():
				for zeile in fileinput.input (datei, inplace=1):
					if zeile.startswith("Refer:") and (zeile.split()[1] == altes_Encoding.split()[3]):
						neuer_inhalt = zeile.split()
						neuer_inhalt[1] = Encoding.split()[3]
						neuer_inhalt[2] = Encoding.split()[2]
						print " ".join(neuer_inhalt)
					else:
						print zeile,
		except subprocess.CalledProcessError:
			None
		
		if name_uebernehmen:
			try:
				#for datei in os.listdir(self.ordner):
				for datei in subprocess.check_output([
						"grep -le \"Substitution.* " + quelle + "\" " + self.ordner + "/*.glyph"
					], shell=True).split():
					for zeile in fileinput.input (datei, inplace=1):
						if zeile.startswith("Substitution") and zeile.endswith(" " + quelle + "\n"):
							if datei!=zieldatei:
								print zeile[:-len(quelle)-1] + ziel
						else:
							print zeile,
			except subprocess.CalledProcessError:
				None
			
			try:
				#for datei in os.listdir(self.ordner):
				for datei in subprocess.check_output([
						"grep -le \"Ligature.* " + quelle + "\" " + self.ordner + "/*.glyph"
					], shell=True).split():
					for zeile in fileinput.input (datei, inplace=1):
						if zeile.startswith("Ligature") and quelle in zeile.split():
							print zeile.replace(quelle,ziel)
						else:
							print zeile,
			except subprocess.CalledProcessError:
				None


	def subtable_loeschen(self, subtable):
		in_chainsub = False
		i = 0
		while i < len(self.props):
			zeile = self.props[i]
			if zeile.startswith("ChainSub2: "):
				if '"'+subtable+'"' in zeile:
					in_chainsub = True
					self.props.pop(i)
					continue
			elif in_chainsub:
				if zeile.startswith("EndFPST"):
					in_chainsub = False
				self.props.pop(i)
				continue
			elif zeile.startswith("Lookup:"):
				vorklammer, _, nachersterklammer = zeile.partition("{")
				klammerinhalt, _, nachklammer = nachersterklammer.partition("}")
				if subtable in klammerinhalt:
					links, _, rechts = klammerinhalt.partition('"' + subtable + '" ')
					if rechts.startswith('("'):
						rechts = rechts.partition(' " ) ')[2]
					zeile = vorklammer + "{" + links + rechts + "}" + nachklammer
			i += 1
		
		try:
			#for datei in os.listdir(self.ordner):
			for datei in subprocess.check_output(["grep -l \"" + subtable + "\" " + self.ordner + "/*"], shell=True).split():
				if datei.endswith(".glyph"):
					for zeile in fileinput.input (datei, inplace=1):
						if '"'+subtable+'"' in zeile:
							continue
						else:
							print zeile,
		except subprocess.CalledProcessError:
			None

	def feature_loeschen (self, feature):
		subtables = []
		i=0
		while i < len(self.props):
			zeile = self.props[i]
			if zeile.startswith("Lookup:"):
				if zeile.partition('"')[2].partition('"')[0] == feature:
					klammerinhalt = zeile.partition('{')[2].partition('}')[0]
					while klammerinhalt:
						if klammerinhalt[0] == "(":
							klammerinhalt = klammerinhalt.partition('" ) ')[2]
						elif klammerinhalt[0] == '"':
							neue_subtable, _, klammerinhalt = klammerinhalt[1:].partition('" ')
							subtables += [neue_subtable]
						elif klammerinhalt[0] == ' ':
							klammerinhalt = klammerinhalt[1:]
						else:
							print "Fehler bei Auslesen von Subtables eines Features\n" + zeile + "\n" + klammerinhalt + "\n\n"
					self.props.pop(i)
					continue
			i+=1
		
		for subtable in subtables:
			self.subtable_loeschen(subtable)


	def feature_aendern(self, feature, alt, neu):
		for i,zeile in enumerate(self.props):
			if zeile.startswith("Lookup:"):
				if zeile.partition('"')[2].partition('"')[0] == feature:
					self.props[i] = zeile.replace("'"+alt+"'", "'"+neu+"'")

	def loeschen(self, ziel):
		self.in_kerns_ersetzen(ziel)
		self.aus_subs_entfernen(ziel)
		
		os.remove(self.ordner + "/" + glyph_nach_datei(ziel))
		
		try:
			#for datei in os.listdir(self.ordner):
			for datei in subprocess.check_output([
					"grep -le \"Substitution.* " + ziel + "\" " + self.ordner + "/*.glyph"
				], shell=True).split():
				for zeile in fileinput.input (datei, inplace=1):
					if zeile.startswith("Substitution") and zeile.endswith(" " + ziel + "\n"):
						pass
					else:
						print zeile,
		except subprocess.CalledProcessError:
			None
		
		try:
			#for datei in os.listdir(self.ordner):
			for datei in subprocess.check_output([
					"grep -le \"Ligature.*" + ziel + "\" " + self.ordner + "/*.glyph"
				], shell=True).split():
				for zeile in fileinput.input (datei, inplace=1):
					if zeile.startswith("Ligature") and ziel in zeile.split():
						pass
					else:
						print zeile,
		except subprocess.CalledProcessError:
			None
	
	def glyphs(self):
		for datei in os.listdir(self.ordner):
			if datei.endswith(".glyph"):
				yield datei_nach_glyph(datei)
	
	def PUA_durch_Verknuepfungen_ersetzen(self):
		for glyph in self.glyphs():
			if glyph.startswith("uni"):
				for zeile in open(self.ordner + "/" + glyph_nach_datei(glyph), "r"):
					nummern = []
					if zeile.startswith("Refer: "):
						nummern += [zeile.split()[1]]
					if len(nummern) == 1:
						grepergebnis = subprocess.check_output([
								"grep -le \"Encoding: .* " + nummern[0] + "$\" " + self.ordner + "/*.glyph"
							], shell=True).split()
						if len(grepergebnis) == 1:
							self.ersetzen(
									glyph,
									datei_nach_glyph(grepergebnis[0].replace(self.ordner+"/","")),
									False
								)
						else:
							raise Exception("Two glyphs with apparantly same encoding:\n" + str(grepergebnis))

					elif len(nummern) != 0:
						raise Exception("PUA glyph with more than one reference.")
	
	def klonen(self, quelle, ucode):
		quelldatei = glyph_nach_datei(quelle)
		for zeile in fileinput.input (self.ordner + "/" + quelldatei, inplace=1):
			print zeile,
			if zeile.startswith("Encoding:"):
				print "AltUni2: 00" + ucode + ".ffffffff.0"

	def umbenennen_und_umkodieren(self, quelle, ziel, neuer_code):
		quelldatei = glyph_nach_datei(quelle)
		zieldatei = glyph_nach_datei(ziel)
		
		shutil.move(self.ordner + "/" + quelldatei, self.ordner + "/" + zieldatei)
		for zeile in fileinput.input (self.ordner + "/" + zieldatei, inplace=1):
			if zeile.startswith("Encoding:"):
				k = int(neuer_code, 16)
				print "Encoding: %i %i " % (k, k) + zeile.split()[3]
			elif zeile.startswith("StartChar:"):
				print "StartChar: " + ziel
			else:
				print zeile,
		
		self.in_kerns_ersetzen(quelle, ziel)
		self.aus_subs_entfernen(quelle)

	def ersetzen_durch_Kompositglyph(self, ziel, teil1, teil2):
		teile = (teil1,teil2)
		breiten = []
		encodings = []
		hstems = ["",""]
		vstems = ["",""]
		dstems = ["",""]
		
		self.props_oeffnen()
		in_kerningtabelle = True
		anzahl_vor = None
		kerning_start = None
		indizes = [None, None]
		j = None
		kerning = 0
		for i,zeile in enumerate(self.props):
			if zeile.startswith("KernClass2"):
				in_kerningtabelle = True
				anzahl_vor = int(zeile.split()[1])
				j = anzahl_vor-1
				anzahl_nach = int(zeile.split()[2])
				kerning_start = i
			elif in_kerningtabelle:
				if zeile.startswith(" "):
					if ("{}" in zeile):
						if all(indizes):
							a = indizes[0] - kerning_start
							b = indizes[1] - kerning_start - anzahl_vor + 1
							kerning = int(zeile.split("{}")[a*anzahl_nach+b])
					else:
						inhalt = zeile.split()[1:]
						if teile[j>0] in inhalt:
							inhalt += [ziel]
						if teile[j<=0] in inhalt:
							indizes[j<=0] = i
						neuer_inhalt = " ".join(inhalt)
						self.props[i] = " " + str(len(neuer_inhalt)) + " " + neuer_inhalt + "\n"
						j -= 1
						continue
				
				in_kerningtabelle = False
				kerning_start = None
				anzahl_vor = None
				indizes = [None, None]
				j = None

		
		for i,teil in enumerate(teile):
			for zeile in open(self.ordner + "/" + glyph_nach_datei(teil), "r"):
				if zeile.startswith("Width:"):
					breiten += [int(zeile.split()[1])]
				elif zeile.startswith("Encoding:"):
					encodings += [zeile.split()[2:]]
				elif zeile.startswith("HStem:"):
					hstems[i] = stems_zerlegen(zeile[7:-1])
				elif zeile.startswith("VStem:"):
					vstems[i] = stems_zerlegen(zeile[7:-1])
				elif zeile.startswith("DStem2:"):
					dstems[i] = stems_zerlegen(zeile[8:-1])
		
		
		zieldatei = glyph_nach_datei(ziel)
		
		verschiebung = breiten[0]+kerning
		
		for hstem in hstems[1]:
			for position in hstem[1]:
				for i in (0,1):
					position[i] = str(string_auswerten(position[i]) + verschiebung)
		
		for vstem in vstems[1]:
			vstem[0][0] = str(string_auswerten(vstem[0][0]) + verschiebung)
		
		for dstem in dstems[1]:
			for i in (0,2):
				dstem[0][i] = str(string_auswerten(dstem[0][i]) + verschiebung)
		
		for zeile in fileinput.input (self.ordner + "/" + zieldatei, inplace=1):
			if (
					   zeile.startswith("StartChar:")
					or zeile.startswith("Encoding:")
					or zeile.startswith("VWidth:")
					or zeile.startswith("GlyphClass:")
					or zeile.startswith("Flags:")
					or zeile.startswith("EndChar")
				):
				print zeile,
			elif zeile.startswith("Fore"):
				print zeile,
				print "Refer: %s %s N 1 0 0 1 0 0 2" % (encodings[0][1], encodings[0][0])
				print "Refer: %s %s N 1 0 0 1 %s 0 2" % (encodings[1][1], encodings[1][0], verschiebung)
			elif zeile.startswith("Width:"):
				print "Width: %i" % (sum(map(int, breiten))+kerning)
			elif zeile.startswith("LayerCount:"):
				print zeile,
				
				stemstring = stems_nach_string(stems_vereinen(hstems))
				if stemstring:
					print "HStem: " + stems_nach_string(stems_vereinen(hstems))
					
				stemstring = stems_nach_string(stems_vereinen(vstems))
				if stemstring:
					print "VStem: " + stems_nach_string(stems_vereinen(vstems))
					
				stemstring = stems_nach_string(stems_vereinen(dstems))
				if stemstring:
					print "DStem2: " + stems_nach_string(stems_vereinen(dstems))
