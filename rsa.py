import sys
import os
import struct
import bigPrimes

# Given two integers a and b, return a tuple (g, x, y), where
# g is gcd(a, b), and ax + by = g
# Code found at https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y	

# Compute the multiplicative inverse mod n of e
# NOTE THAT e must be greater than log_2(n) in
# order to assure there a block gets encrypted. This
# fact comes from section 7D of the RSA paper.

# Note that n here represents Euler's totient of n, and
# e represents the public key in RSA
def findMultiplicativeInverse(e, n):
	multInv = egcd(e, n)[1]

	return multInv


# Tests if findMultiplicativeInverse(e, n) is correct
def testMultInv():
	a = 11
	b = 60

	assert(findMultiplicativeInverse(a, b) == 11)

	a = 157
	b = 2668

	assert(findMultiplicativeInverse(a, b) == 17)


def makeCharGroups(asciiInt):
	asciiStr = str(asciiInt)
	charGroups = []
	skip1 = False
	skip2 = False

	if len(asciiStr) < 2: #handle case where asciiInt is just a single char value
		charNum = asciiStr[0]
		charGroups.append(int(charNum))
		return charGroups
	if len(asciiStr) < 3: # same thing but with 3 digit char value
		charNum = asciiStr[0] + asciiStr[1]
		charGroups.append(int(charNum))
		return charGroups

	for i in xrange(0, len(asciiStr)):
		if skip2:
			skip2 = False
			continue
		if skip1:
			skip1 = False
			continue

		charNum = asciiStr[i] + asciiStr[i + 1]
		skip1 = True
		if charNum == "10" or charNum == "11" or charNum == "12":
			charNum = charNum + asciiStr[i + 2]
			skip2 = True
		charGroups.append(int(charNum))
	return charGroups


def convertTextToASCII(text):
	ascii = ""
	for i in xrange(0, len(text)):
		ascii = ascii + str(ord(text[i]))
	asciiInt = int(ascii)
	return asciiInt

def convertASCIIToText(ascii):
	charGroups = makeCharGroups(ascii)
	text = ""

	for char in charGroups:
		text = text + chr(char)
	return text

# choose a public keys e, n
def createPubKey(p, q):

	n = p * q
	return 65537, n

# create private key d given the public key e, n and large primes p and q
def createPrivKey(e, n, p, q):
	totientP = p - 1
	totientQ = q  - 1
	totientN = totientP * totientQ

	return findMultiplicativeInverse(e, totientN)


# splits the input word into 2-character chunks, and returns a list of these chunks
def chunkifyString(string):
	if len(string) <= 64:
		return string
	else:
		return string[0:64] + chunkifyString(string[64:])


# Tests to see if RSA encryption decryption works as expected
def testRSA():
	testString = "This is my test string, isn't it great?!"
	encrypted = encrypt(testString)

	print "encrypted string is " + stringifyEncryptedData(encrypted)

	decrypted = decrypt(encrypted)
	finalChunkedString = map(convertASCIIToText, decrypted)

	print "original string is " + str(testString)
	print "decrypted string is " + ''.join(finalChunkedString)


# Given a list of 2-letter characters, encrypt each using the public key
def mapEncryption(listOfASCII, e, n):
	encryptedList = []
	for chunk in listOfASCII:
		encryptedList.append(pow(chunk, e, n))

	return encryptedList

# Given a list of ascii longs, convert them to strings and append them to form one string
def stringifyEncryptedData(asciiList):
	outputStr = ""
	for ascii in asciiList:
		outputStr = outputStr + str(ascii)
	return outputStr


# Given the text to encrypt and the public key, returns a list of the encrypted blocks
def encrypt(text, e, n):
	chunkedString = chunkifyString(text)
	asciiChunkedString = map(convertTextToASCII, chunkedString)

	encrypted = mapEncryption(asciiChunkedString, e, n)

	return encrypted

# Given a list of encrypted blocks, decrypt each using the private key and return
# the plaintext as a string
def decrypt(encryptedBlocks, d, n):
	decryptedList = []
	for chunk in encryptedBlocks:
		decryptedList.append(str(pow(long(chunk), d, n)))
		
	finalChunkedString = map(convertASCIIToText, decryptedList)
	return ''.join(finalChunkedString)

# returns a tuple of (e, d) and primes (p, q) of a RSA private/public keypair
def getPubPrivKeyPair():
	d = 0

	(p, q) = getPAndQ()
	(e, n) = createPubKey(p, q)
	d = createPrivKey(e, n, p, q)

	return (e, d), (p, q)


# Returns two large primes
def getPAndQ():

	p = bigPrimes.getLargePrime()
	q = bigPrimes.getLargePrime()
	return p, q

# Tests ascci conversion
def testASCCIConversion():
	string = "this is my string"

	ascci = convertTextToASCII(string)
	backToString = convertASCIIToText(ascci)

	assert(string == backToString)

# print proper usage of program
def showUsage():
	print "usage: python rsaimplement.py argument1 [argument2, argument3, argument4]"
	print "the three valid arguments are:"
	print "'keygen'                    This will generate a public (e, n) and private (d, n) keypair for you to use"
	print "'--encrypt text e n         This will encrypt text using the public keypair (e, n) and print the list of the encrypted blocks"
	print "'--decrypt text d n         This will decrypt text using the private keypair (d, n) and print the decrypted string"

if __name__ == "__main__":

	if len(sys.argv) > 1:
		option = sys.argv[1]
		if option == ("--encrypt" or "-e") and len(sys.argv) == 5:
			print "the ciphertext list is: " + str(encrypt(sys.argv[2], int(sys.argv[3]), int(sys.argv[4])))

		elif ((sys.argv[1] == "--decrypt") or (sys.argv[1] == "-d")) and  len(sys.argv) == 5:
			chunkString = sys.argv[2][1:-1]
			chunkList = chunkString.split(',')
			chunkList = map(long, chunkList)
			print "the plaintext is: " + decrypt(chunkList, int(sys.argv[3]), int(sys.argv[4]))

		elif option == "keygen":
			print "Calculating private/public keypair. This may take several seconds..."
			(e,d), (p,q) = getPubPrivKeyPair()
			print "the public key is: " + "(" + str(e) + ", " + str(p*q) + ")"
			print "the private key is: " + "(" + str(d) + ", " + str(p*q) + ")"

		else:
			showUsage()
	else:
		showUsage()



