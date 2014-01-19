#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

def to_sensible_html(string):
	newstring = re.sub(r'\n', '', string)
	regexp = re.compile(r'<p.*>.*</p>')
	matchobj = regexp.search(newstring)
	return newstring[matchobj.start():matchobj.end()]

def description_to_tex(string):
	# remove <p...>
	c = (re.sub(r'<p(.*?)>', '', string, count = 0)).replace('</p>','')
	# replace '<span style=\" text-decoration: underline;\">'
	c = re.sub(r'<(span).*?(underline).*?>(?P<underlined>.*?)</span>', r'$\\underbar{\g<underlined>}$', c, count=0)
	# rid ourselves of the non underline spans <span style=" font-family:'Sans Serif';">
	c = re.sub(r'<(span).*?>(?P<text>.*?)</span>', r' \g<text>', c, count=0)
	# Replace spaces with \: -- lets you add words now
	# Turn "o- $\underbar{Ph}OMe PMP" into "o- $\underbar{Ph}OMe\: PMP"
	# Turn " $\underbar{H}-13 and  $\underbar{H}-18" into " $\underbar{H}-13\: and\:  $\underbar{H}-18"
	spaces = re.compile(r"(?P<first>.)" # Starts with any character except newline, capture as "first"
	r" "# With a space in the middle
	r"(?=\w)" # Ends with any alphanumeric character, lookahead.
	)
	c = spaces.sub('\g<1>\\: ',c) # Substitute spaces with the letter before the space and "\:"
	# Now do the ands
	c = c.replace('and ', 'and\\: ')
	c = c.replace('or ', 'or\\: ')

	if c[-1] == '}':
		c += '$' # If its at the end of the string, it causes trouble

	sbonds = re.compile(r"\s*" # Any amount of whitespace. It wont compile with whitespace before a \sbond in \ce{}
	r"-" # A single bond
	r"\s*" # Any amount of whitespace
	r"(?P<numbers>\d+)" # Some numbers, then store in the numbers group
	)
	c = sbonds.sub('\\sbond $\g<1>$', c) # replace -NUMBER with "\sbond $NUMBER$" in math mode, to prevent superscripts
	
	dbonds = re.compile(r"\s*" # Any amount of whitespace. It wont compile with whitespace before a \sbond in \ce{}
	r"=" # A double bond
	r"\s*" # Any amount of whitespace
	r"(?P<numbers>\d+)" # Some numbers, then store in the numbers group
	)
	c = sbonds.sub('\\dbond $\g<1>$', c) # replace -NUMBER with "\dbond $NUMBER$" in math mode, to prevent superscripts
	
	splitnums = re.compile(r"(?P<first>\d+)" # A Number, repeated any amount of times
	r"\$/" # The Dollar sign, then a forward slash
	r"(?P<second>\d+)" # A Number, repeated any amount of times
	)
	c = splitnums.sub('\g<1>/\g<2>$', c) # Now move the digits in "$20$/21" to "$20/21$"
	
	## Replace "NUM$'" with "NUM'$" -- corrects problems where prime turns to comma
	primes = re.compile(r"(?P<number>\d+)"# A number
	r"\$\w*'" # The dollar sign, any whitespace, the quote "'"
	)
	c = primes.sub('\g<1>\'$', c)
	
	# Now replace '-' with 'single' and '=' with 'double' bonds
	# Spaces before \sbond, etc throw errors when compiling the tex.
	c = c.replace(' -', '\\sbond ').replace(' =', '\\dbond ') # With spaces
	c = c.replace('-', '\\sbond ').replace('=', '\\dbond ') # Without spaces
	return '\ce{%s}' %c
