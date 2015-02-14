# -*- coding: utf-8 -*-

# Author:
# 	Erik Vido, https://github.com/erikvido
#
# Source-code:
#	https://github.com/erikvido/latex_converter.git 
#
# Copyright:
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import os
import re
import codecs

USAGE="""
USAGE: python convert.py <source> [encoding] [<dest>] 

	source -- The path to the original file

	encoding -- File-encoding of source, e.g. utf-8 (default). On linux-based systems
		The encoding can be checked with the file-command:
			> file -I <filename>

	dest -- Where the converted file will be written (optional).
		If dest is not given, than it will be call the same as
		source, but with an ending _converted, e.g. <source>_converted

DESCRIPTION:
	Reads source-file and replaces characters with special meading in latex
	with their latex-correspondance.
"""

# The following is a map from unicode-characters given in hex-code
# to its correspondig latex representation. Note, that the latex-correspondance
# is given as Python-Raw-Type (prevents need to escape backslashes).
# 
# Not all possible mappings are yet inserted, feel free to add more.
# 
# For unicode lookup see:
# 	http://unicodelookup.com/
# A list of latex symbols can be found here:
#	http://www.rpi.edu/dept/arc/training/latex/LaTeX_symbols.pdf
#	ftp://ftp.dante.de/tex-archive/biblio/biber/documentation/utf8-macro-map.html
# 	http://consult.wikidot.com/latex#accent
latex_equivalents = {

	# Copied from unicode_mapping.py
	0xC0: r'\`{A}', # À
	0xC1: r'\’{A}', # Á
	0xC2: r'\^{A}', # Â
	0xC3: r'\~{A}', # Ã
	0xC4: r'\"{A}', # Ä
	0xC5: r'\AA', # Å
	0xC6: r'\AE', # Æ
	0xC7: r'\c{C}', # Ç
	0xD0: r'\DH', # Ð
	0xD6: r'\"{O}', # Ö
	0xDC: r'\"{U}', # Ü
	0xDE: r'\TH', # Þ alternative r'\Thorn'
	0xDF: r'\ss', # ß
	0xE0: r'\`{a}', # à
	0xE1: "\'{a}", # á
	0xE2: r'\^{a}', # â
	0xE3: r'\~{a}', # ã
	0xE5: r'\aa', # å
	0xE6: r'\ae', # æ
	0xE9: r"\'{e}", # é
	# End of 'Copied from unicode_mapping.py'

	0x151: r'\H{o}',
	0x15F: r'\c{s}',
	0x105: r'\k{a}',
	0x101: r'\={a}',
	0x1E35: r'\b{k}',
	0x117: r'\.{e}',
	0x1E43: r'\d{m}',
	0x103: r'\u{a}',
	0x10D: r'\v{c}',
	
	0xB0: r'\textdegree',

	0x300: r'\`',
	0x301: r'\'',

	0xF0: r'\dh',
	0xF6: r'\"o',
	0xF8: r'\o',
	0xFC: r'\"u',
	0xFE: r'\textthorn',
	0xFE: r'\textthornvari',
	0xFE: r'\textthornvarii',
	0xFE: r'\textthornvariii',
	0xFE: r'\textthornvariv',
	0xFE: r'\th',
	0x110: r'\DJ',
	0x111: r'\dj',
	0x111: r'\textcrd',
	0x126: r'\textHbar',
	0x127: r'\textcrh',
	0x127: r'\texthbar',
	0x131: r'\i',
	0x237: r'\j',
	0x132: r'\IJ',
	0x133: r'\ij',
	0x138: r'\textkra',
	0x141: r'\L',
	0x142: r'\textbarl',
	0x142: r'\l',
	0x14A: r'\NG',
	0x14B: r'\ng',
	0x152: r'\OE',
	0x153: r'\oe',
	0x1F: r'\_',
	0x5F: r'\_',
	0x24: r'\$',
	0x25: r'\%',
	0x26: r'\&',
	0xA9: r'\copyright',
	0x2026: r'\dots',

	# Greek alphabeth
	0x3B1: r'\alpha',
	0x3B2: r'\beta',
	0x3B3: r'\gamma',
	0x3B4: r'\delta',
	0x3B5: r'\varepsilon',
	0x3B6: r'\zeta',
	0x3B7: r'\eta',
	0x3B8: r'\vartheta',
	0x3B9: r'\iota',
	0x3BA: r'\kappa',
	0x3BB: r'\lambda',
	0x3BC: r'\mu',
	0x3BD: r'\nu',
	0x3BE: r'\xi',
	0x3BF: r'\omicron',
	0x3C0: r'\pi',
	0x3C1: r'\varrho',
	0x3C2: r'\varsigma',
	0x3C3: r'\sigma',
	0x3C4: r'\tau',
	0x3C5: r'\upsilon',
	0x3C6: r'\varphi',
	0x3C7: r'\chi',
	0x3C8: r'\psi',
	0x3C9: r'\omega',
	0x391: r'\Alpha',
	0x392: r'\Beta',
	0x393: r'\Gamma',
	0x394: r'\Delta',
	0x395: r'\Epsilon',
	0x396: r'\Zeta',
	0x397: r'\Eta',
	0x398: r'\Theta',
	0x399: r'\Iota',
	0x39A: r'\Kappa',
	0x39B: r'\Lambda',
	0x39C: r'\Mu',
	0x39D: r'\Nu',
	0x39E: r'\Xi',
	0x39F: r'\Omicron',
	0x3A0: r'\Pi',
	0x3A1: r'\Rho',
	0x3A3: r'\Sigma',
	0x3A4: r'\Tau',
	0x3A5: r'\Upsilon',
	0x3A6: r'\Phi',
	0x3A7: r'\Chi',
	0x3A8: r'\Psi',
	0x3A9: r'\Omega',
}

_latex_equivalents_mapping = dict( (unichr(k), v.decode('utf-8')) for k,v in latex_equivalents.items())

def convert(input):
	"""
	Returns unicode with all occurences in latex_equivalents-mapping replaced.

	Arguments:
	input -- unicode
	"""
	output = []
	for c in input:
		if c in _latex_equivalents_mapping:
			output.append(_latex_equivalents_mapping[c])
		else:
			output.append(c)

	return u''.join(output)

def run(orig, target, encoding):
	"""
	Reads each line from 'orig' and writes it to 'target' after conversion.
	'target' will have the same file-encoding as 'orig'

	Arguments:
	orig -- Path to source-file
	target -- Path to destination-file
	encoding -- the file-encoding of the source-file, e.g. 'utf-8'
	"""
	with codecs.open(orig, mode='r', encoding=encoding) as source:
		with codecs.open(target, mode='w', encoding=encoding) as dest:
			for line in source: # line is unicode 
				dest.write(convert(line))

def target_from_source(filepath):
	"""
	Adds '_converted' to the filename (before suffix)

	Arguments:
	filepath -- The file-path
	"""
	dirname = os.path.dirname(filepath)
	filename = os.path.basename(filepath)
	fileparts = filename.rsplit('.', 1)

	target = fileparts[0] + '_converted'
	if len(fileparts) > 1:
		target += "." + fileparts[1]

	return os.path.join(dirname, target)


if __name__ == '__main__':
	if len(sys.argv) < 2: 
		sys.exit(USAGE)

	orig = sys.argv[1]

	if 'help' == orig or '-h' == orig:
		sys.exit(USAGE)

	if not os.path.isfile(orig):
		sys.exit('Cannot find file: ' + orig)

	encoding = sys.argv[2] if len(sys.argv) > 2 else 'utf-8' 
	target = target_from_source(orig) if len(sys.argv) < 4 else sys.argv[3]

	run(orig, target, encoding)

	print('Wrote to file: ' + target)
