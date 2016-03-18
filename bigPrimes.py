from random import SystemRandom
from fractions import gcd
rand = SystemRandom()

numberOfDigits = 150
numberOfTests = 100



def testForPrimality(b):
	for i in xrange(1,numberOfTests):
		a = rand.randint(1,b-1)
		if(gcd(a,b) != 1):
			#print("Failed mod test in round "+str(i))
			return False
		j = Jacobi(a,b)%b
		jTest = powMod(a,(b-1)/2,b)
		if j != jTest:
			#print("Failed Jacobi test in round "+str(i))
			return False
	return True

def Jacobi(a,b):
	if a == 1:
		return 1
	elif a%2 == 0:
		return Jacobi(a/2,b)*pow(-1, (b*b-1)/8)
	else:
		return Jacobi(b%a, a)*pow(-1, (a-1)*(b-1)/4)

def powMod(base, power, mod):
	powerBinary = (bin(power)[2:])[::-1] #horrible hack to reverse string
	powers = [0]*len(powerBinary)

	currentValue = base%mod
	for i in range(0,len(powers)):
		powers[i] = currentValue
		currentValue = (currentValue*currentValue)%mod
	result = 1
	for i in range(0,len(powers)):
		if int(powerBinary[i]) == 1:
			result = (result*powers[i])%mod
	return result

# create a large random prime
def getLargePrime():
	bigRandomInt = (2*rand.randint(pow(10,numberOfDigits),pow(10,numberOfDigits+1)))+1
	while (testForPrimality(bigRandomInt) == False):
		bigRandomInt = (2*rand.randint(pow(10,numberOfDigits),pow(10,numberOfDigits+1)))+1
	return bigRandomInt

# if __name__ == "__main__":
# 	print(getLargePrime())