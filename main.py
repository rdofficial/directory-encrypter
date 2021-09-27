"""
main.py - Directory Encrypter

Created by : Rishav Das (https://github.com/rdofficial/)
Created on : September 20, 2021

Last modified by : Rishav Das (https://github.com/rdofficial/)
Last modified on : September 27, 2021

Changes made in the last modifications :
1. Removed the error of rendering the list of contents in a directory, thus making the enryption process more error free.

Authors contributed to this script (Add your name below if you have contributed) :
1. Rishav Das (github:https://github.com/rdofficial/, email:rdofficial192@gmail.com)
"""

# Importing the required functions and modules
from os import path, listdir, rename, chdir, remove
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

	def start_encryption(self, directory = None, recursive = False):
		""" This method / function serves the functionality of encrypting each of the files in the directory tree, and then saving them back. This function uses the class variables in order to execute the task properly, also a config file is created by the which contains the details of the encryption by then. """

		# Setting the directory to the user specified if not recalled
		if directory == None:
			directory = self.directory

		# Changing the current working directory to the user specified directory
		chdir(directory)

		# Creating the config file in the user specified directory
		if recursive:
			pass
		else:
			config = self.encrypt(text = self.password)
			open('.config_encryption', 'w+').write(config)
			del config

		# Creating a list of the contents in the current directory
		# ----
		items = listdir()
		file_list = []
		dir_list = []

		for item in items:
			if path.isfile(item):
				# If the currently iterated item is a file, then we append it to the file list

				file_list.append(item)
			elif path.isdir(item):
				# If the currently iterated item is a directory, then we append it to the directory list

				dir_list.append(item)

		for item in dir_list:
			# Appending items from dir_list to the file_list

			file_list.append(item)

		items = file_list
		del file_list, dir_list
		# ----

		# Encrypting each files in the current directory
		for file in items:
			# Iterating each of the contents of the directory

			if file == '.config_encryption':
				# If teh currently iterated item is the config file, then we skip the part

				continue
			elif path.isfile(file):
				# If the currently iterated item is a file, then we continue to encrypt it

				# Encrypting its contents and saving it back
				chdir(directory)
				contents = open(file, 'r').read()
				contents = self.encrypt(text = contents)
				open(file, 'w+').write(contents)
				del contents

				# Renaming the file after encrypting its contents
				newname = self.encrypt(text = file)
				newname = newname.replace('/', '#')
				rename(file, newname)
				del newname

				# Displaying the message of a file being encrypted
				print(f'[#] File encrypted : {path.join(directory, file)}')
			elif path.isdir(file):
				# If the currently iterated item is a directory, then we continue to decrypt it

				# Re-calling the function with opening the sub-folder
				directory = path.join(directory, file)
				print(f'[$] Moving inside a directory : {directory}')
				self.start_encryption(directory = directory, recursive = True)
			else:
				# If the currently iterated item is neither a file nor a directory, then we raise a fucking error with a custom message

				raise TypeError(f'{path.join(directory, file)} is neither a file nor a directory.')

	def start_decryption(self, directory = None, recursive = False):
		""" This method / function serves the functionality of decrypting each of the files in the directory tree, and then saving them back. This function uses the class variables in order to execute the task properly, also it rechecks the config file information with the user entered credentials. """

		# Setting the directory to the user specified if not recalled
		if directory == None:
			directory = self.directory

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

				remove('.config_encryption')
			else:
				# If the passwords fail to match, then we raise a fucking error with a custom message

				raise ValueError(f'Incorrect password for the encrypted folder "{self.directory}"')

		# Creating a list of the contents in the current directory
		# ----
		items = listdir()
		file_list = []
		dir_list = []

		for item in items:
			if path.isfile(item):
				# If the currently iterated item is a file, then we append it to the file list

				file_list.append(item)
			elif path.isdir(item):
				# If the currently iterated item is a directory, then we append it to the directory list

				dir_list.append(item)

		for item in dir_list:
			# Appending items from dir_list to the file_list

			file_list.append(item)

		items = file_list
		del file_list, dir_list
		# ----

		# Encrypting each files in the current directory
		for file in items:
			# Iterating each of the contents of the directory

			if file == '.config_encryption':
				# If teh currently iterated item is the config file, then we skip the part

				continue
			elif path.isfile(file):
				# If the currently iterated item is a file, then we continue to decrypt it

				# Decrypting the contents and saving it back
				contents = open(file, 'r').read()
				contents = self.decrypt(text = contents)
				open(file, 'w+').write(contents)
				del contents

				# Renaming the file after decrypting its contents
				newname = file.replace('#', '/')
				newname = self.decrypt(text = newname)
				rename(file, newname)
				del newname
			elif path.isdir(file):
				# If the currently iterated item is a directory, then we continue to decrypt it

				# Re-calling the function with opening the sub-folder
				directory = path.join(directory, file)
				self.start_decryption(directory = directory, recursive = True)
			else:
				# If the currently iterated item is neither a file nor a directory, then we raise a fucking error with a custom message

				raise TypeError(f'{path.join(directory, file)} is neither a file nor a directory.')

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

def main():
	# Asking the user to enter the directory location for encryption / decryption
	directory = input('Enter the directory location : ')

	# Asking the user to enter a password for the encryption / decryption
	password = input('Enter the password for encryption / decryption : ')

	# Creating an directory encrypter object in order to work properly
	encrypter = DirectoryEncrypter(password, directory)

	# Asking the user the choice of whether to encrypt or to decrypt
	choice = input('\nChoose an option :\n1. Encrypt\n2. Decrypt\nEnter your choice : ')

	if choice == '1':
		# If the user chooses the option to encrypt the specified directory, then we continue

		encrypter.start_encryption()
	elif choice == '2':
		# If the user chooses the optio to decrypt the specified directory, then we continue

		encrypter.start_decryption()
	else:
		# If the the user chooses an unavailable option, then we raise an error with custom message

		raise ValueError('No such options available')

	# Displaying the message on console screen after the processes are done executing
	print('\n[ Process completed ]')

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		# If the user presses CTRL+C key combo, then we exit the script

		exit()
	except Exception as e:
		# If there are any errors encountered during the process, then we display the error message on the console screen and exit

		print(f'[ Error : {e} ]')