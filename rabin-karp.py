import random
from Crypto.Util import number
import sys
import ast

# Compute (a*b) mod n


def mod_multiply(a, b, n):
    res = 0  # Initialize result
    # Update a if it is more than or equal to n
    a = a % n
    while (b):
        if (b & 1):
            res = (res + a) % n

        a = (2 * a) % n
        b >>= 1
    return res


class Window():
    def __init__(self, text, pattern, prime, radix=256):
        self.text = text
        self.pattern = pattern
        self.m = len(pattern)  # For convenience
        self.n = prime
        self.cur_pos = 0
        self.radix = radix
        # Used to shift the window
        self.msb_value = pow(radix, len(pattern) - 1, prime)
        self.cur_hash_t = self.get_hash(text)
        self.hash_p = self.get_hash(pattern)

    def get_hash(self, string):
        window = string[self.cur_pos:self.m]
        sum = 0
        for i in window:
            # Compute sum = {sum*radix + ascii(i)} mod n
            sum = (mod_multiply(sum, self.radix, self.n) + ord(i)) % self.n
        return sum

    def shift_one(self):
        if self.cur_pos + self.m >= len(self.text):
            self.cur_pos += 1
            return
        # Shift window by 1
        # Calculate {cur_hash_t - (text[cur_pos] * msb_value)} + text[cur_pos + m]} mod n
        multiplicand = self.cur_hash_t - \
            ord(self.text[self.cur_pos]) * self.msb_value
        self.cur_hash_t = (
            mod_multiply(self.radix, multiplicand, self.n)
            + ord(self.text[self.cur_pos + self.m]))  # % self.n
        self.cur_pos += 1

    def is_matched(self):
        return self.cur_hash_t == self.hash_p

    def __str__(self):
        return 'Cur Pos: {}, Cur Hash T: {}, Hash P: {}'.format(self.cur_pos, self.cur_hash_t, self.hash_p)


def find_next_shift(text, window):
    while (not window.is_matched()) and (window.cur_pos <= len(text) - window.m):
        window.shift_one()

    if window.is_matched():
        return window.cur_pos
    return -1


def get_rand(nbits):
    return number.getPrime(nbits)


def pretty_print_shift(s, m, text, pre_post=5):
    pr = 'Valid Shift Found! Position = {}, Context: '.format(s)
    l = max(0, s - pre_post)        
    r = min(s + m + pre_post, len(text))

    pr += text[l:max(0, s)]
    pr += ' >> ' + text[s:s+m] + ' << '
    pr += text[min(len(text), s+m):r]
    print(pr)


def veryfy_shifts(textfile, pfile, shiftfile):
    text = ''
    with open(textfile) as f:
        for l in f.readlines():
            text += l
        f.close()
    
    pattern = ''
    with open(pfile) as f:
        for l in f.readlines():
            pattern += l
        f.close()

    shifts = ''
    with open(shiftfile) as f:
        shifts = f.readline().strip()
        f.close()
    shifts = shifts.replace('Valid Shift Positions: ', '')
    shifts = ast.literal_eval(shifts)

    pos = 0
    org_shifts = []
    while pos >= 0:
        pos = text.find(pattern, pos)
        if pos >= 0:
            org_shifts.append(pos)
            pos += 1
    
    if org_shifts == shifts:
        print('Shifts are identical')
    else:
        print('Failed to verify Shifts. Original number of Shifts: {}, Identified: {}'.format(org_shifts, shifts))


def rabin_karp(textfile, pfile, outfile='out.txt', nbits=32, radix=256):
    prime = get_rand(nbits)

    text = ''
    with open(textfile) as f:
        for l in f.readlines():
            text += l
        f.close()

    pattern = ''
    with open(pfile) as f:
        for l in f.readlines():
            pattern += l
        f.close()

    if len(text) < len(pattern):
        print('The pattern is longer than the text! No Valid Shifts')
        return

    print('Prime modulus chosen: {}'.format(prime))
    window = Window(text, pattern, prime, radix=radix)
    shift_pos = []
    spurios_pos = []
    while window.cur_pos <= (len(text) - len(pattern)):
        s = find_next_shift(text, window)
        if s >= 0:
            # Verify if it is valid
            if text[s:s+len(pattern)] == pattern:
                pretty_print_shift(s, len(pattern), text)
                shift_pos.append(s)
            else:
                print('Spurious hit at s = {}, text = {}'.format(
                    s, text[s: s+window.m]))
                spurios_pos.append(s)

            window.shift_one()
    
    if outfile:
        with open(outfile, 'w') as f:
            f.write('Valid Shift Positions: {}\nSpurious Shifts: {}'.format(shift_pos, spurios_pos))
            f.close()
    
    return shift_pos, spurios_pos

if __name__ == '__main__':
    args = sys.argv
    arglen = len(args)

    if arglen < 4:
        print('Usage: {} {} {} {} {} {} {}'.format(
            args[0], 'match|verify', '<Text In File>', '<Pattern File>', '[Out File]', '[Radix]', '[Prime Bit Length]')
            )
        exit()
    
    infile = args[2]
    pattern = args[3]
    
    radix = 256
    nbits = 32
    outfile = None
    
    if args[1].lower() == 'match':
        if arglen == 5:
            outfile = args[4]

        if arglen == 6:
            radix = args[5]

        if arglen == 7:
            outfile = args[6]
        
        rabin_karp(textfile=infile, pfile=pattern, outfile=outfile, nbits=nbits, radix=radix)
    elif args[1].lower() == 'verify':
        if arglen < 5:
            print('Usage: {} {} {} {} {}'.format(args[0], args[1], '<Text File>', '<Pattern File>', '<Shifts File>'))
        
        shiftsfile = args[4]
        veryfy_shifts(infile, pattern, shiftsfile)
    else:
        print('Usage: {} {} {} {} {} {} {}'.format(
            args[0], 'match|verify', '<Text In File>', '<Pattern File>', '[Out File]', '[Radix]', '[Prime Bit Length]')
            )

