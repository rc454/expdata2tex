#!/usr/bin/python
# -*- coding: utf-8 -*-

class data_IR():
	IR_frequency=''
	IR_strength="s"
	data=[(IR_frequency,IR_strength)]
	def add_update(self, index, freq, stren):
		if index > (len(self.data) -1):
			self.data.append((freq, stren))
		elif index <= (len(self.data)-1):
			self.data[index]=(freq, stren)
	def toString(self):
		outbits=[]
		for i in self.data:
			outbits.append(','.join(i))
		return '|'.join(outbits)
	def fromString(self, string):
		self.data=[] # Clear the container
		for i in string.split('|'):
			self.data.append(tuple(i.split(',')))
	def __repr__(self):
		for i in self.data:
			return '%s,%s' %(i[0], i[1])
	def __len__(self):
		return len(self.data)
	def __iter__(self):
		for i in self.data:
			yield i
	def isEmpty(self):
		if len(self.data) == 1 and (self.data[0][0] == 0.0 or self.data[0][0] == ''):
			return True
		else:
			return False

class AD():
	AD_specificrotation=0.0
	AD_concentration=0.0
	AD_solvent = "CHCl3"
	data=(AD_specificrotation, AD_concentration, AD_solvent)
	def insert(self, _rotation, _concentration, _solvent):
		self.data=(_rotation, _concentration, _solvent)
	def __repr__(self):
		return '%s,%s,%s' %self.data
class proton_data():
	proton_shift = 0.0
	proton_protons = 0
	proton_multiplicity = ""
	proton_coupling = []
	proton_identity = ""
	data=[(proton_shift, proton_protons, proton_multiplicity, proton_coupling, proton_identity)]
	def __len__(self):
		return len(self.data)
	def add_update(self, index, shift, protons, multiplicity, coupling, iden):
		if index > (len(self.data) -1):
			self.data.append((shift, protons, multiplicity, coupling, iden))
		elif index <= (len(self.data)-1):
			self.data[index]=(shift, protons, multiplicity, coupling, iden)
	def toString(self):
		outbits=[]
		for i in self.data:
			outbits.append('¬'.join(i))
		return '|'.join(outbits)
	def fromString(self, string):
		self.data=[] # Clear the container
		for i in string.split('|'):
			self.data.append(tuple(i.split('¬')))
	def __repr__(self):
		for i in self.data:
			return '%s, %s, %s, %s, %s|' %(i[0], i[1], i[2], i[3], i[4])
	def __iter__(self):
		for i in self.data:
			yield i
	def isEmpty(self):
		if len(self.data) == 1 and (self.data[0][0] == 0.0 or self.data[0][0] == ''):
			return True
		else:
			return False


class proton_specinfo():
	proton_frequency=0.0
	proton_solvent='Chloroform-d1'
	def __repr__(self):
		return "%s,%s" %(self.proton_frequency, self.proton_solvent)

class carbon_data():
	carbon_shift = 0.0
	carbon_identity = ""
	data=[(carbon_shift, carbon_identity)]
	def __len__(self):
		return len(self.data)
	def add_update(self, index, shift, iden):
		if index > (len(self.data) -1):
			self.data.append((shift, iden))
		elif index <= (len(self.data)-1):
			self.data[index]=(shift, iden)
	def toString(self):
		outbits=[]
		for i in self.data:
			outbits.append('¬'.join(i))
		return '|'.join(outbits)
	def fromString(self, string):
		self.data=[] # Clear the container
		for i in string.split('|'):
			self.data.append(tuple(i.split('¬')))
	def __repr__(self):
		for i in self.data:
			return '%s,%s|' %(i[0], i[1])
	def __iter__(self):
		for i in self.data:
			yield i
	def isEmpty(self):
		if len(self.data) == 1 and (self.data[0][0] == 0.0 or self.data[0][0] == ''):
			return True
		else:
			return False
			

class carbon_specinfo():
	carbon_frequency=0.0
	carbon_solvent='Chloroform-d1'
	def __repr__(self):
		return "%s,%s" %(self.carbon_frequency, self.carbon_solvent)

class mother():
	_data_IR = data_IR()
	_AD = AD()
	_proton_data = proton_data()
	_proton_specinfo = proton_specinfo()
	_carbon_data = carbon_data()
	_carbon_specinfo = carbon_specinfo()
	
	def __iter__(self):
		for i in [self._data_IR, self._AD, self._proton_data, self._proton_specinfo, self._carbon_data, self._carbon_specinfo]:
			yield i