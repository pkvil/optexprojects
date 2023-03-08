#! /usr/bin/env python
# -*- coding: utf-8 -*-

from manipulation import *

M20 = Schrift("UnifrakturMaguntia20", "UnifrakturMaguntia.sfdir")

M20.PUA_durch_Verknuepfungen_ersetzen()

# Geviertstrich statt Halbgeviertstrich:
M20.loeschen("endash")
M20.klonen("emdash", "2013")

# Lang-s-Automatik standardmäßig aktivieren:
M20.feature_aendern("'cv11' long s", "cv11", "liga")

for glyph in M20.glyphs():
	# Versalziffern zum Standard machen:
	if (glyph.endswith(".uppercase") and glyph!="one.uppercase"):
		M20.ersetzen(glyph[:-10], glyph)
	elif glyph.endswith(".upper"):
		M20.ersetzen(glyph[:-6], glyph)
	
	# Glyphen löschen, die nicht zur Verfügung standen oder nur für Features relevant sind:
	elif (
				glyph.endswith(".alt2")
				or glyph.endswith(".swash")
				or glyph.endswith(".modern")
				or glyph.endswith(".modern2")
				or glyph.endswith(".upper")
				or ("grave" in glyph)
				or ("acute" in glyph)
				or ("circumflex" in glyph)
				or glyph.endswith("tilde")
				or glyph.endswith("tildecomb")
				or (glyph.endswith("ring") and glyph!="ring")
				or ("cedilla" in glyph)
				or (glyph.endswith("slash") and glyph!="slash" and glyph!="percentslash")
				or ("macron" in glyph)
				or ("ogonek" in glyph)
				or ("breve" in glyph)
				or (("dotaccent" in glyph) and glyph!="dotaccent" and glyph!="dotaccent.liga")
				or ("dotcomb" in glyph)
				or ("caron" in glyph)
				or ("commaaccent" in glyph)
				or ("hungarumlaut" in glyph)
				or ("commasubcomb" in glyph)
				or glyph.endswith("stroke")
				or glyph.startswith("arrow")
				or glyph.endswith(".tab")
				or glyph.endswith(".uppertab")
			):
		M20.loeschen(glyph)

M20.umbenennen_und_umkodieren("one.uppercase", "one", "0031")

M20.loeschen("dollar")
M20.loeschen("at")
M20.loeschen("cent")
M20.loeschen("sterling")
M20.loeschen("yen")
M20.loeschen("copyright")
M20.loeschen("registered")
M20.loeschen("micro")
M20.loeschen("Eth")
M20.loeschen("eth")
M20.loeschen("Thorn")
M20.loeschen("thorn")
M20.loeschen("Hbar")
M20.loeschen("hbar")
M20.loeschen("IJ")
M20.loeschen("ij")
M20.loeschen("kra")
M20.loeschen("ldot")
M20.loeschen("AE")
M20.loeschen("ae")
M20.loeschen("OE")
M20.loeschen("oe")
M20.loeschen("commaturnedabovecomb")
M20.loeschen("Schwa")
M20.loeschen("schwa")
M20.loeschen("perthousand")
M20.loeschen("pertenthousand")
M20.loeschen("trademark")
M20.loeschen("a32")
M20.loeschen("longs_b")
M20.loeschen("longs_h")
M20.loeschen("longs_j")
M20.loeschen("f_j")
M20.loeschen("f_f_j")
M20.loeschen("f_dotlessj")
M20.loeschen("f_dotlessij")
M20.loeschen("f_f_dotlessj")
M20.loeschen("longs_ij")
M20.loeschen("f_ij")
M20.loeschen("s.noswash")
M20.loeschen("ringcomb")

M20.loeschen("Edieresis")
M20.loeschen("edieresis")
M20.loeschen("Idieresis")
M20.loeschen("idieresis")
M20.loeschen("Wdieresis")
M20.loeschen("wdieresis")
M20.loeschen("Ydieresis")
M20.loeschen("dieresiscomb")
M20.loeschen("s_dieresiscomb")


# Nicht-automatisch aktive Features löschen

M20.feature_loeschen("'cv20' Swashless s")
M20.feature_loeschen("'cv16' Alternate sdieresis composition")
M20.feature_loeschen("'aalt' Access All Alternates")
M20.feature_loeschen("'pnum' Proportional Numbers")
M20.feature_loeschen("'tnum' Tabular Numbers")
M20.feature_loeschen("'onum' Lowercase Numbers")
M20.feature_loeschen("'lnum' Uppercase Numbers")
M20.feature_loeschen("'ss01' Modern variants")
M20.feature_loeschen("'ss03' Iji to Jij")
M20.feature_loeschen("'cv00/40' No long s")
M20.feature_loeschen("'cv01' Modern k")
M20.feature_loeschen("'cv02' Modern x")
M20.feature_loeschen("'cv03' Modern y")
M20.feature_loeschen("'cv04' Modern A")
M20.feature_loeschen("'cv05' Modern G")
M20.feature_loeschen("'cv06' Modern K")
M20.feature_loeschen("'cv07' Modern N")
M20.feature_loeschen("'cv08' Modern S")
M20.feature_loeschen("'cv09' Modern V")
M20.feature_loeschen("'cv10' Modern Y")
M20.feature_loeschen("'cv13' I to J")
M20.feature_loeschen("'cv14' Ae, Oe, Ue")
M20.feature_loeschen("'cv15' a^e, o^e, u^e")
M20.feature_loeschen("'cv16' s diacritcs with swash")
M20.feature_loeschen("'cv17' s diacritics with long s")
M20.feature_loeschen("'cv18' Alternative d and t with caron")
M20.feature_loeschen("'cv19' en dash to em dash")
M20.feature_loeschen("'cv21' sacute alternates")
M20.feature_loeschen("'cv22' scircumflex alternates")
M20.feature_loeschen("'cv23' scaron alternates")
M20.feature_loeschen("'cv24' sdotaccent alternate")
M20.feature_loeschen("'cv25' sdiaeresis alternate")
M20.feature_loeschen("'cv26' Alternative d with caron")
M20.feature_loeschen("'cv27' Alternative t with caron")
M20.feature_loeschen("'cv28' Double lslash and longsslash ligatures")
M20.feature_loeschen("'dlig' Double m/n to m/n with macron")

M20.props_schliessen()

M19 = Schrift("UnifrakturMaguntia19", "UnifrakturMaguntia20.sfdir")
M18 = Schrift("UnifrakturMaguntia18", "UnifrakturMaguntia20.sfdir")
M17 = Schrift("UnifrakturMaguntia17", "UnifrakturMaguntia20.sfdir")
M16 = Schrift("UnifrakturMaguntia16", "UnifrakturMaguntia20.sfdir")


for M in [M19,M20]:
	M.loeschen("ecomb")
	M.loeschen("adieresis.alt")
	M.loeschen("odieresis.alt")
	M.loeschen("udieresis.alt")

M20.feature_loeschen("'xxxx' et to rrot")
M20.loeschen("e_t")

M20.props_schliessen()

for M in [M16,M17,M18,M19]:
	M.feature_aendern("'hlig' etc to et-rrot", "hlig", "clig")
	M.ersetzen_durch_Kompositglyph("Adieresis", "A", "e")
	M.ersetzen_durch_Kompositglyph("Odieresis", "O", "e")

	M.loeschen("I")
	M.klonen("J", "0049")

for M in [M18,M19]:
	M.ersetzen_durch_Kompositglyph("Udieresis", "U", "e")

for M in [M16,M17,M18]:
	M.ersetzen("adieresis", "adieresis.alt")
	M.ersetzen("odieresis", "odieresis.alt")
	M.ersetzen("udieresis", "udieresis.alt")
	M.loeschen("ydieresis")
	M.loeschen("longs_odieresis")

for M in [M20,M19,M18]:
	for glyph in M.glyphs():
		if glyph.endswith(".hist"):
			M.loeschen(glyph)

for M in [M17,M16]:
	M.loeschen("U")
	M.klonen("V", "0055")
	M.feature_aendern("'ss02' Uvu to Vuv", "ss02", "liga")
	M.ersetzen_durch_Kompositglyph("Udieresis", "V", "e")


for M in [M20,M19,M18,M17]:
	M.loeschen("r.round")

M16.feature_aendern("'cv12' rrotunda", "cv12", "liga")

for M in [M20,M19,M18,M17,M16]:
	for glyph in M.glyphs():
		if glyph.endswith(".alt"):
			M.loeschen(glyph)
	
	M.feature_loeschen("'cv12' rrotunda")
	M.feature_loeschen("'ss02' Uvu to Vuv")
	M.feature_loeschen("'hlig' etc to et-rrot")
	
	M.props_schliessen()