#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import fontforge
import io
import time

def decide_deletion(existing_folders):
	if existing_folders:
		yesno = "X"
		if len(sys.argv) > 1:
			if sys.argv[1] == "-f":
				yesno = "Y"
		while yesno not in ["Y", "N"]:
			yesno = raw_input("Really delete the following folders? (Y|N)\n" + "\n".join(existing_folders) + "\n").upper()
		if yesno == "N":
			print "Aborting"
			sys.exit(0)
	for folder in existing_folders:
		shutil.rmtree(folder)

date = time.strftime("%Y-%m-%d")

def include_license(font):
	sfnt_names = list(font.sfnt_names)
	assert sfnt_names[-1][1] == 'License'
	license_sfnt = list(sfnt_names.pop(-1))
	license_sfnt[2] = io.open('OFL.txt', encoding='utf8').read()
	sfnt_names.append(tuple(license_sfnt))
	font.sfnt_names = sfnt_names

def compile_font(sfdir, ttf):
	font = fontforge.open(sfdir)
	font.selection.all()
	font.autoInstr()
	font.fontlog = io.open('FontLog.txt', encoding='utf8').read()
	font.version = date
	include_license(font)
	font.generate(ttf)
	font.close()

folders = ["UnifrakturMaguntia%i.sfdir" % i for i in range(16,22)]
existing_folders = [folder for folder in folders if folder in os.listdir(".")]
decide_deletion(existing_folders)

import make_modern_variant
import make_old_variants

fonts = ["UnifrakturMaguntia"+str(x) for x in range(16,22)+[""]]

for font in fonts:
	sfdir = font + ".sfdir"
	ttf = font + ".ttf"
	autohint = font + "_autohint.ttf"
	compile_font(sfdir, ttf)
	os.system("ttfautohint -c -n " + ttf + " " + autohint)
	shutil.move(autohint, ttf)




