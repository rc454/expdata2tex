#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

def to_sensible_html(string):
	remove_newlines = re.compile(r'\n')
	newstring = remove_newlines.sub('', string)
	regexp = re.compile(r'<p.*>.*</p>')
	matchobj = regexp.search(newstring)
	return newstring[matchobj.start():matchobj.end()]

def description_to_tex(string):
	remove_start_p = re.compile(r'\[<p\](.*?)\[</p>\]') # Needs to be first match of >
	new_string = string[(string.find('>')+1):string.rfind('</p>')]
	c = new_string.replace('<span style=\" text-decoration: underline;\">', ' $\\underbar{').replace('</span>','}')
	string_out=''
	for segment in c.split('}'):# replace the }'s depending on the next character
		if segment == '': # If its at the end of the string, it causes trouble
			string_out += '}$ '
		else:
			if segment[0].isdigit() and c.split('}').index(segment) !=0:
				string_out += '}$_' + segment 
			elif c.split('}').index(segment) !=0:
				string_out += '}$ ' + segment
			elif c.split('}').index(segment) ==0:
				string_out += segment
				
	# So, to prevent a number after \sbond becoming subscript, it must be placed in math mode.
	tmpstring = ''
	singles = re.compile(r"(-\d+)|(=\d+)") # Matches = or - followed by any number of digits
	
	starts_ends = [match.span() for match in re.finditer(singles, string_out)] # Generates a list of tuples that span the regex match for singles and doubles (bonds)
	# Check if starts_ends is not empty
	if len(starts_ends) != 0:
		tmpstring += string_out[:starts_ends[0][0]] # Add the begining of the string up until the match
		for item in starts_ends:
			tmpstring += string_out[item[0]] # Add the bond character - or =
			if (item[0] + 1) == item[1]: # If it is a single digit, add that digit
				tmpstring += ('$' + string_out[item[1]] + '$')
			else: # Add all the other digits
				tmpstring += ('$' + string_out[(item[0]+1):item[1]] + '$')
		# Add the rest of the string, if it isnt at the end
		if starts_ends[-1][1] < (len(string_out)+1):
			tmpstring += string_out[starts_ends[-1][1]:]
		string_out = tmpstring
	

	# Now replace '-' with 'single' and '=' with 'double' bonds
	# Spaces before \sbond, etc throw errors when compiling the tex.
	string_out = string_out.replace(' -', '\\sbond ').replace(' =', '\\dbond ') # With spaces
	string_out = string_out.replace('-', '\\sbond ').replace('=', '\\dbond ') # Without spaaces
	
	
	return '\ce{%s}' %string_out
