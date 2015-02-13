# Author:
# 	Erik Vido <erik.vido@gmx.ch>
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
USAGE: python convert.py <source> [<dest>] [encoding]

	source --	The path to the original file
	dest -- 	Where the converted file will be written (optional).
		If dest is not given, than it will be call the same as
		source, but with an ending _converted, e.g. <source>_converted
	encoding -- File-encoding of source, e.g. utf-8 (default). On linux-based systems
		The encoding can be checked with the file-command:

			> file -I <filename>

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
#     http://unicodelookup.com/
# A list of latex symbols can be found here:
#     http://www.rpi.edu/dept/arc/training/latex/LaTeX_symbols.pdf
#     ftp://ftp.dante.de/tex-archive/biblio/biber/documentation/utf8-macro-map.html
latex_equivalents = {
	unichr(0x300): r'\`',
	unichr(0x301): r'\'',
	unichr(0x302): r'\^',
	unichr(0x303): r'\~',
	unichr(0x304): r'\=',
	unichr(0x307): r'\.',
	unichr(0x308): r'\'',
	unichr(0xC4): r'\"A',
	unichr(0xC5): r'\AA',
	unichr(0xC6): r'\AE',
	unichr(0xD0): r'\DH',
	unichr(0xD6): r'\"O',
	unichr(0xD8): r'\O',
	unichr(0xDC): r'\"U',
	unichr(0xDE): r'\Thorn',
	unichr(0xDE): r'\TH',
	unichr(0xDF): r'\ss',
	unichr(0xE4): r'\"a',
	unichr(0xE5): r'\aa',
	unichr(0xE6): r'\ae',
	unichr(0xF0): r'\dh',
	unichr(0xF6): r'\"o',
	unichr(0xF8): r'\o',
	unichr(0xFC): r'\"u',
	unichr(0xFE): r'\textthorn',
	unichr(0xFE): r'\textthornvari',
	unichr(0xFE): r'\textthornvarii',
	unichr(0xFE): r'\textthornvariii',
	unichr(0xFE): r'\textthornvariv',
	unichr(0xFE): r'\th',
	unichr(0x110): r'\DJ',
	unichr(0x111): r'\dj',
	unichr(0x111): r'\textcrd',
	unichr(0x126): r'\textHbar',
	unichr(0x127): r'\textcrh',
	unichr(0x127): r'\texthbar',
	unichr(0x131): r'\i',
	unichr(0x237): r'\j',
	unichr(0x132): r'\IJ',
	unichr(0x133): r'\ij',
	unichr(0x138): r'\textkra',
	unichr(0x141): r'\L',
	unichr(0x142): r'\textbarl',
	unichr(0x142): r'\l',
	unichr(0x14A): r'\NG',
	unichr(0x14B): r'\ng',
	unichr(0x152): r'\OE',
	unichr(0x153): r'\oe',
	unichr(0x166): r'\textTbar',
	unichr(0x166): r'\textTstroke',
	unichr(0x167): r'\texttbar',
	unichr(0x167): r'\texttstroke',
	unichr(0x180): r'\textcrb',
	unichr(0x181): r'\textBhook',
	unichr(0x186): r'\textOopen',
	unichr(0x187): r'\textChook',
	unichr(0x188): r'\textchook',
	unichr(0x188): r'\texthtc',
	unichr(0x189): r'\textDafrican',
	unichr(0x18A): r'\textDhook',
	unichr(0x18E): r'\textEreversed',
	unichr(0x190): r'\textEopen',
	unichr(0x191): r'\textFhook',
	unichr(0x192): r'\textflorin',
	unichr(0x194): r'\textGammaafrican',
	unichr(0x195): r'\texthvlig',
	unichr(0x195): r'\hv',
	unichr(0x196): r'\textIotaafrican',
	unichr(0x198): r'\textKhook',
	unichr(0x199): r'\textkhook',
	unichr(0x199): r'\texthtk',
	unichr(0x19B): r'\textcrlambda',
	unichr(0x19D): r'\textNhookleft',
	unichr(0x1A0): r'\OHORN',
	unichr(0x1A1): r'\ohorn',
	unichr(0x1A4): r'\textPhook',
	unichr(0x1A5): r'\textphook',
	unichr(0x1A5): r'\texthtp',
	unichr(0x1A9): r'\textEsh',
	unichr(0x1A9): r'\ESH',
	unichr(0x1AA): r'\textlooptoprevesh',
	unichr(0x1AB): r'\textpalhookbelow',
	unichr(0x1AC): r'\textThook',
	unichr(0x1AD): r'\textthook',
	unichr(0x1AD): r'\texthtt',
	unichr(0x1AE): r'\textTretroflexhook',
	unichr(0x1AF): r'\UHORN',
	unichr(0x1B0): r'\uhorn',
	unichr(0x1B2): r'\textVhook',
	unichr(0x1B3): r'\textYhook',
	unichr(0x1B4): r'\textyhook',
	unichr(0x1B7): r'\textEzh',
	unichr(0x1DD): r'\texteturned',
	unichr(0x250): r'\textturna',
	unichr(0x251): r'\textscripta',
	unichr(0x252): r'\textturnscripta',
	unichr(0x253): r'\textbhook',
	unichr(0x253): r'\texthtb',
	unichr(0x254): r'\textoopen',
	unichr(0x254): r'\textopeno',
	unichr(0x255): r'\textctc',
	unichr(0x256): r'\textdtail',
	unichr(0x256): r'\textrtaild',
	unichr(0x257): r'\textdhook',
	unichr(0x257): r'\texthtd',
	unichr(0x258): r'\textreve',
	unichr(0x259): r'\textschwa',
	unichr(0x25A): r'\textrhookschwa',
	unichr(0x25B): r'\texteopen',
	unichr(0x25B): r'\textepsilon',
	unichr(0x25C): r'\textrevepsilon',
	unichr(0x25D): r'\textrhookrevepsilon',
	unichr(0x25E): r'\textcloserevepsilon',
	unichr(0x25F): r'\textbardotlessj',
	unichr(0x260): r'\texthtg',
	unichr(0x261): r'\textscriptg',
	unichr(0x262): r'\textscg',
	unichr(0x263): r'\textgammalatinsmall',
	unichr(0x263): r'\textgamma',
	unichr(0x264): r'\textramshorns',
	unichr(0x265): r'\textturnh',
	unichr(0x266): r'\texthth',
	unichr(0x267): r'\texththeng',
	unichr(0x268): r'\textbari',
	unichr(0x269): r'\textiotalatin',
	unichr(0x269): r'\textiota',
	unichr(0x26A): r'\textsci',
	unichr(0x26B): r'\textltilde',
	unichr(0x26C): r'\textbeltl',
	unichr(0x26D): r'\textrtaill',
	unichr(0x26E): r'\textlyoghlig',
	unichr(0x26F): r'\textturnm',
	unichr(0x270): r'\textturnmrleg',
	unichr(0x271): r'\textltailm',
	unichr(0x272): r'\textltailn',
	unichr(0x272): r'\textnhookleft',
	unichr(0x273): r'\textrtailn',
	unichr(0x274): r'\textscn',
	unichr(0x275): r'\textbaro',
	unichr(0x276): r'\textscoelig',
	unichr(0x277): r'\textcloseomega',
	unichr(0x278): r'\textphi',
	unichr(0x279): r'\textturnr',
	unichr(0x27A): r'\textturnlonglegr',
	unichr(0x27B): r'\textturnrrtail',
	unichr(0x27C): r'\textlonglegr',
	unichr(0x27D): r'\textrtailr',
	unichr(0x27E): r'\textfishhookr',
	unichr(0x27F): r'\textlhti',
	unichr(0x280): r'\textscr',
	unichr(0x281): r'\textinvscr',
	unichr(0x282): r'\textrtails',
	unichr(0x283): r'\textesh',
	unichr(0x284): r'\texthtbardotlessj',
	unichr(0x285): r'\textraisevibyi',
	unichr(0x286): r'\textctesh',
	unichr(0x287): r'\textturnt',
	unichr(0x288): r'\textrtailt',
	unichr(0x288): r'\texttretroflexhook',
	unichr(0x289): r'\textbaru',
	unichr(0x28A): r'\textupsilon',
	unichr(0x28B): r'\textscriptv',
	unichr(0x28B): r'\textvhook',
	unichr(0x28C): r'\textturnv',
	unichr(0x28D): r'\textturnw',
	unichr(0x28E): r'\textturny',
	unichr(0x28F): r'\textscy',
	unichr(0x290): r'\textrtailz',
	unichr(0x291): r'\textctz',
	unichr(0x292): r'\textezh',
	unichr(0x292): r'\textyogh',
	unichr(0x293): r'\textctyogh',
	unichr(0x294): r'\textglotstop',
	unichr(0x295): r'\textrevglotstop',
	unichr(0x296): r'\textinvglotstop',
	unichr(0x297): r'\textstretchc',
	unichr(0x298): r'\textbullseye',
	unichr(0x299): r'\textscb',
	unichr(0x29A): r'\textcloseepsilon',
	unichr(0x29B): r'\texthtscg',
	unichr(0x29C): r'\textsch',
	unichr(0x29D): r'\textctj',
	unichr(0x29E): r'\textturnk',
	unichr(0x29F): r'\textscl',
	unichr(0x2A0): r'\texthtq',
	unichr(0x2A1): r'\textbarglotstop',
	unichr(0x2A2): r'\textbarrevglotstop',
	unichr(0x2A3): r'\textdzlig',
	unichr(0x2A4): r'\textdyoghlig',
	unichr(0x2A5): r'\textdctzlig',
	unichr(0x2A6): r'\texttslig',
	unichr(0x2A7): r'\textteshlig',
	unichr(0x2A7): r'\texttesh',
	unichr(0x2A8): r'\texttctclig',
	unichr(0x2BE): r'\hamza',
	unichr(0x2BF): r'\ain',
	unichr(0x2BF): r'\ayn',
	unichr(0x2C8): r'\textprimstress',
	unichr(0x2D0): r'\textlengthmark',
	unichr(0x2010): r'\-',
	unichr(0x2011): r'\-',
	unichr(0x2012): r'\textendash',
	unichr(0x2012): r'\--',
	unichr(0x2013): r'\textendash',
	unichr(0x2013): r'\--',
	unichr(0x2014): r'\textemdash',
	unichr(0x2014): r'\---',
	unichr(0x2018): r'\textquoteleft',
	unichr(0x2019): r'\textquoteright',
	unichr(0x201A): r'\quotesinglbase',
	unichr(0x201C): r'\textquotedblleft',
	unichr(0x201D): r'\textquotedblright',
	unichr(0x201E): r'\quotedblbase',
	unichr(0x2020): r'\dag',
	unichr(0x2021): r'\ddag',
	unichr(0x2022): r'\textbullet',
	unichr(0x2026): r'\dots',
	unichr(0x2030): r'\textperthousand',
	unichr(0x2031): r'\textpertenthousand',
	unichr(0x2039): r'\guilsinglleft',
	unichr(0x203A): r'\guilsinglright',
	unichr(0x203B): r'\textreferencemark',
	unichr(0x203D): r'\textinterrobang',
	unichr(0x203E): r'\textoverline',
	unichr(0x27E8): r'\langle',
	unichr(0x27E9): r'\rangle',
	unichr(0x22): r'\textquotedbl',
	unichr(0x24): r'\textdollar',
	unichr(0x25): r'\textpercent',
	unichr(0x26): r'\textampersand',
	unichr(0x27): r'\textquotesingle',
	unichr(0x2A): r'\textasteriskcentered',
	unichr(0x3C): r'\textless',
	unichr(0x3E): r'\textgreater',
	unichr(0x5C): r'\textbackslash',
	unichr(0x5E): r'\textasciicircum',
	unichr(0x5F): r'\textunderscore',
	unichr(0x60): r'\textasciigrave',
	unichr(0x7C): r'\textbar',
	unichr(0x7E): r'\textasciitilde',
	unichr(0xA0): r'\nobreakspace',
	unichr(0xA1): r'\textexclamdown',
	unichr(0xA2): r'\textcent',
	unichr(0xA3): r'\textsterling',
	unichr(0xA3): r'\pounds',
	unichr(0xA4): r'\textcurrency',
	unichr(0xA5): r'\textyen',
	unichr(0xA6): r'\textbrokenbar',
	unichr(0xA7): r'\textsection',
	unichr(0xA7): r'\S',
	unichr(0xA8): r'\textasciidieresis',
	unichr(0xA9): r'\textcopyright',
	unichr(0xA9): r'\copyright',
	unichr(0xAA): r'\textordfeminine',
	unichr(0xAB): r'\guillemotleft',
	unichr(0x2212): r'\textminus',
	unichr(0xAE): r'\textregistered',
	unichr(0xAF): r'\textasciimacron',
	unichr(0xB0): r'\textdegree',
	unichr(0xB2): r'\texttwosuperior',
	unichr(0xB3): r'\textthreesuperior',
	unichr(0xB4): r'\textasciiacute',
	unichr(0xB6): r'\textparagraph',
	unichr(0xB6): r'\P',
	unichr(0xB7): r'\textcentereddot',
	unichr(0xB7): r'\textperiodcentered',
	unichr(0xB8): r'\textasciicedilla',
	unichr(0xB9): r'\textonesuperior',
	unichr(0xBA): r'\textordmasculine',
	unichr(0xBB): r'\guillemotright',
	unichr(0xBC): r'\textonequarter',
	unichr(0xBD): r'\textonehalf',
	unichr(0xBE): r'\textthreequarters',
	unichr(0xBF): r'\textquestiondown',
	unichr(0x3B1): r'\alpha',
	unichr(0x3B2): r'\beta',
	unichr(0x3B3): r'\gamma',
	unichr(0x3B4): r'\delta',
	unichr(0x3B5): r'\varepsilon',
	unichr(0x3B6): r'\zeta',
	unichr(0x3B7): r'\eta',
	unichr(0x3B8): r'\vartheta',
	unichr(0x3B9): r'\iota',
	unichr(0x3BA): r'\kappa',
	unichr(0x3BB): r'\lambda',
	unichr(0x3BC): r'\mu',
	unichr(0x3BD): r'\nu',
	unichr(0x3BE): r'\xi',
	unichr(0x3BF): r'\omicron',
	unichr(0x3C0): r'\pi',
	unichr(0x3C1): r'\varrho',
	unichr(0x3C2): r'\varsigma',
	unichr(0x3C3): r'\sigma',
	unichr(0x3C4): r'\tau',
	unichr(0x3C5): r'\upsilon',
	unichr(0x3C6): r'\varphi',
	unichr(0x3C7): r'\chi',
	unichr(0x3C8): r'\psi',
	unichr(0x3C9): r'\omega',
	unichr(0x391): r'\Alpha',
	unichr(0x392): r'\Beta',
	unichr(0x393): r'\Gamma',
	unichr(0x394): r'\Delta',
	unichr(0x395): r'\Epsilon',
	unichr(0x396): r'\Zeta',
	unichr(0x397): r'\Eta',
	unichr(0x398): r'\Theta',
	unichr(0x399): r'\Iota',
	unichr(0x39A): r'\Kappa',
	unichr(0x39B): r'\Lambda',
	unichr(0x39C): r'\Mu',
	unichr(0x39D): r'\Nu',
	unichr(0x39E): r'\Xi',
	unichr(0x39F): r'\Omicron',
	unichr(0x3A0): r'\Pi',
	unichr(0x3A1): r'\Rho',
	unichr(0x3A3): r'\Sigma',
	unichr(0x3A4): r'\Tau',
	unichr(0x3A5): r'\Upsilon',
	unichr(0x3A6): r'\Phi',
	unichr(0x3A7): r'\Chi',
	unichr(0x3A8): r'\Psi',
	unichr(0x3A9): r'\Omega',
}


def convert(input):
	"""
	Returns a string with all occurences of unicode-characters found
	in the latex_equivalents-mapping replaced by the mapping.

	Arguments:
	input -- string (unicode) 
	"""
	output = []
	for c in input:
		if c in latex_equivalents:
			output.append(latex_equivalents[c])
		else:
			output.append(c)

	return ''.join(output)

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
			for line in source:
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

	target = target_from_source(orig) if len(sys.argv) < 3 else sys.argv[2]
	encoding = sys.argv[3] if len(sys.argv) == 4 else 'utf-8' 

	run(orig, target, encoding)

	print('Wrote to file: ' + target)
