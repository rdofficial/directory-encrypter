	"""
main.py - Directory Encrypter

Created by : Rishav Das (https://github.com/rdofficial/)
Created on : September 20, 2021

Last modified by : -
Last modified on : -

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
from os import path, listdir, rename, chdir
from base64 import b64encode, b64decode
from sys import platform

class DirectoryEncrypter:
	"""
This class serves the functionality of encrypting the entire directory specified by the user with a password. Also, the directory serves the feature of decrypting the contents of the directory back too. This class uses its own encryption algorithm, so if the password is lost then no other encryption services might be able to restore the directory back to its normal state.

This class creates a config file in the directory post the encryption process, which marks certain details that are required during the decryption of the directory. The contents of the config file are further hashed in order to store its privacy of certain information. """

	def __init__(self, password, directory):
		# Defining the class variables
		self.password = password
		self.directory = directory
		self.key = None

		# Validating some of the user entered parameters
		# ----
		# Validating the user specified password
		if type(self.password) == str:
			# If the user entered password is of string type, then we continue for further validation

			if len(self.password) > 5:
				# If the user entered password has character length of more than 5, then we continue

				pass
			else:
				# If the user entered password has character length not more than 5, then we raise an error with a custom message

				raise SyntaxError(f'{self.password} is not of valid character length. The length of the password should be more than 5 characters.')
		else:
			# If the user entered password is not of string type, then we raise an error with a custom message

			raise TypeError(f'{self.password} is not of string type. The password should be of string format.')

		# Validating the user specified directory
		if path.isdir(self.directory):
			# If the user specified directory exists, then we continue

			pass
		else:
			# If the user specified directory doesn't exists, then we raise an error with a custom message

			raise ValueError(f'"{self.directory}" no such directory exists')
		# ----

		# Calling the generateKey() method in order to generate the key for the encryption
		self.generateKey()

	def start_encryption(self, directory = self.directory, recursive = False):
		""" This method / function serves the functionality of encrypting each of the files in the directory tree, and then saving them back. This function uses the class variables in order to execute the task properly, also a config file is created by the which contains the details of the encryption by then. """

		# Changing the current working directory to the user specified directory
		chdir(directory)

		# Creating the config file in the user specified directory
		if recursive:
			pass
		else:
			config = self.encrypt(text = self.password)
			open('.config_encryption', 'w+').write(config)
			del config

		# Encrypting each files in the current directory
		for file in listdir(directory):
			# Iterating each of the contents of the directory

			if path.isfile(file):
				# If the currently iterated item is a file, then we continue to encrypt it

				# Encrypting its contents and saving it back
				contents = open(file, 'r').read()
				contents = self.encrypt(text = contents)
				open(file, 'w+').write(contents)
				del contents

				# Renaming the file after encrypting its contents
				newname = self.encrypt(text = file)
				rename(file, newname)
				del newname
			elif path.isdir(file):
				# If the currently iterated item is a directory, then we continue to decrypt it

				# Re-calling the function with opening the sub-folder
				directory = path.join(directory, file)
				self.start_encryption(directory = directory, recursive = True)
			else:
				# If the currently iterated item is neither a file nor a directory, then we raise a fucking error with a custom message

				raise TypeError(f'{file} is neither a file nor a directory.')

	def start_decryption(self, directory = self.directory, recursive = False):
		""" This method / function. """

		# Changing the current working directory to the user specified directory
		chdir(directory)

		# Checking whether the user specified password and the original password matches or not
		if recursive:
			pass
		else:
			password = self.encrypt(text = self.password)
			config = open('.config_encryption', 'r').read()
			if password == config:
				# If the passwords are matched, then we continue

				pass
			else:
				# If the passwords fail to match, then we raise a fucking error with a custom message

				raise ValueError(f'Incorrect password for the encrypted folder "{self.directory}"')

		# Encrypting each files in the current directory
		for file in listdir(directory):
			# Iterating each of the contents of the directory

			if path.isfile(file):
				# If the currently iterated item is a file, then we continue to decrypt it

				# Decrypting the contents and saving it back
				contents = open(file, 'r').read()
				contents = self.decrypt(text = contents)
				open(file, 'w+').write(contents)
				del contents

				# Renaming the file after decrypting its contents
				newname = self.decrypt(text = file)
				rename(file, newname)
				del newname
			elif path.isdir(file):
				# If the currently iterated item is a directory, then we continue to decrypt it

				# Re-calling the function with opening the sub-folder
				directory = path.join(directory, file)
				self.start_decryption(directory = directory, recursive = True)
			else:
				# If the currently iterated item is neither a file nor a directory, then we raise a fucking error with a custom message

				raise TypeError(f'{file} is neither a file nor a directory.')

	def encrypt(self, text = ''):
		""" This method serves the functionality of encrypting the plain texts with the password stored in the class properties. The function uses the self.key generated key in order to encrypt the text. The key must be generated before calling this function/method in order to prevent any errors. """

		# Checking if the key is already generated or not
		if self.key != None:
			# If the key is defined, then we continue for the fucking encryption process

			# Encrypting the text specified
			# ----
			encryptedText = ''

			for character in text:
				# Iterating through each fucking character in order to fucking encrypt it

				encryptedText += chr((ord(character) + self.key) % 256)

			# Converting the encoding of the text to base64
			encryptedText = b64encode(encryptedText.encode()).decode()

			# Returning back the encrypted text
			return encryptedText
			# ----
		else:
			# If the key is not defined, then we raise a fucking error with a custom message

			raise ReferenceError(f'No key generated yet')

	def decrypt(self, text = ''):
		""" This method serves the functionality of decrypting the already encrypted key, using the key generated. If the key isn't generated before calling thi function, then it might result in some errors. The key is stored as a class property / variable 'self.key'. """

		# Checking if the key is already generated or not
		if self.key != None:
			# If the key is defined, then we contiunue for the fucking decryption process

			# Decrypting the text specified
			# ----
			# Converting the encoding of the text from base64 to utf-8
			text = b64decode(text.encode()).decode()

			decryptedText = ''

			for character in text:
				# Iterating through each fucking character in order to fucking decrypt it

				decryptedText += chr((ord(character) - self.key) % 256)

			# Returning back the decrypted text
			return decryptedText
			# ----
		else:
			# If the key is not defined, then we raise a fucking error with a custom message

			raise ReferenceError(f'No key is generated yet')

	def generateKey(self):
		""" This method serves the functionality of generating the key out of the user specified password for the encryption or decryption process. The function uses the password value stored in the class property / variable 'self.password'. """

		# Generating the key from the encryption using the user entered password for encryption / decryption
		key = 0
		isEven = True

		for i in self.password:
			# Iterating over each character in the encrypted key entered by the user
				
			if isEven:
				# If the current iteration is even number, then we add the char code value

				key += ord(i)
			else:
				# If the current iteration is odd number (not even), then we subtract the char code value

				key -= ord(i)
		del isEven

		# Making the key possitive
		if key < 0:
			# If the key value is less than 0, then we change the negative sign to possitive by simply multiplying it with -1

			key *= (-1)

		# Adding the length of the password to itself
		key += len(self.password)

		# Saving the key to the class property / variable 'self.key'
		self.key = key