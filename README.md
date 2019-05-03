# Implementation of Rabin-Karp String matcher, and the RSA Cryptosystem

## Configuration
Tested on Windows 10, 64 bit <br>
Uses Python 3.6 <br>

## Setup
Run `python -m pip install -r requirements.txt` to install all dependencies for the program. <br>

## Running the Program
The CLI for the program is developed to be separate for RabinKarp as well as RSA. <br>

### Rabin Karp
The general for of the Rabin-Karp CLI is shown below. <br> 
```python
python rabin_karp.py match|verify <Text In File> [<Pattern File>] [Out File] [Radix] [Prime Bit Length]
```
<br>

Some example commands are shown below.
* Find all shifts in file text.txt using the pattern in file pattern.txt <br>
`python rabin_karp.py match text.txt pattern.txt`
* Find all shifts in file text.txt using pattern entered from the keyboard <br>
`python rabin_karp.py match text.txt`
* Find all shifts and save it to a file “out2.txt” <br>
`python rabin_karp.py match text.txt pattern.txt out2.txt`
* Verify all shifts found from file “big.txt” using pattern in file “pattern.txt”, with shifts from the Rabin Karp matcher stored in “out2.txt” <br>
`python rabin_karp.py verify big.txt pattern.txt out2.txt`

### RSA Crypto System
The general form of the CLI for the RSA program are shown below. <br>
```python
python rsa.py genkey|encrypt|decrypt|gendata <Input file> <output file> <Key File>
```
Some example commands are shown <br>
* Generating a Public-Private Keypair of length 64 bit (default), and save to files <keypair_{public|private}.key> <br>
`python rsa.py genkey`
* Generating a Public-Private Keypair of length 128bits, and save it to file “key_{public|private}.key> <br>
`python rsa.py genkey key 128`
* Generating 1000 19 digit numbers at random, and store it to file “cc.txt” <br>
`python rsa.py gendata cc.txt 1000`
* Encrypting file “cc.txt” and saving the output to file “cc_e.txt” using default keypair <br>
`python rsa.py encrypt cc.txt cc_e.txt`
* Decrypting file “cc_e.txt” and save output to file “cc_d.txt” using default keypair <br>
`python rsa.py decrypt cc_e.txt cc_d.txt`
* Decrypting file “cc_e.txt” and save output to file “cc_d.txt” using keypair key2_{public|private}.key <br>
`python rsa.py decrypt cc_e.txt cc_d.txt key2`

## Evaluating Performance
Run `python rk_perf.py` to generate performance graphs for the Rabin Karp algorithm <br>

Run `python rsa_perf.py` to generate performance graphs for the RSA Cryptosystem <br>
