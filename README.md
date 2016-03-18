# slow-rsa
A readable Python implementation of the public key encryption algorithm, RSA.

## Commands
* **keygen** This will generate a public (e, n) and private (d, n) keypair for you to use
    - `python rsa.py keygen`

* **encrypt** This will encrypt text using the public keypair (e, n) and print the list of the encrypted blocks
    - `python rsa.py <text> <e> <n>`

* **decrypt** This will decrypt text using the private keypair (d, n) and print the decrypted string
    - `python rsa.py <text> <d> <n>`


RSA uses several interesting mathematical theorems and algorithms. If you are interested please read

### Further Study
* [RSA](https://en.wikipedia.org/wiki/RSA)
* [Euler's Totient Function](https://en.wikipedia.org/wiki/Euler%27s_totient_function)
* [Fermat's Little Theorem](https://en.wikipedia.org/wiki/Fermat%27s_little_theorem)
