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
	c = new_string.replace('<span style=\" text-decoration: underline;\">', ' \\underbar{').replace('</span>','}')
	string_out=''
	for segment in c.split('}'):# replace the }'s depending on the next character
		if segment == '': # If its at the end of the string, it causes trouble
			string_out += '}'
		else:
			if segment[0].isdigit() and c.split('}').index(segment) !=0:
				string_out += '}_' + segment 
			elif c.split('}').index(segment) !=0:
				string_out += '} ' + segment
			elif c.split('}').index(segment) ==0:
				string_out += segment
	return '\ce{%s}' %string_out
