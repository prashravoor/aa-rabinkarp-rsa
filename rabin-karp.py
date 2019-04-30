import random
from Crypto.Util import number

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


def rabin_karp(text, pattern, outfile='out.txt', nbits=32):
    prime = get_rand(nbits)

    print('Prime modulus chosen: {}'.format(prime))
    window = Window(text, pattern, prime)
    shift_pos = []
    spurios_pos = []
    while window.cur_pos <= (len(text) - len(pattern)):
        s = find_next_shift(text, window)
        x = 10
        if s >= 0:
            # Verify if it is valid
            if text[s:s+len(pattern)] == pattern:
                print('Valid shift found! S = {}, Context: {} >>{}<< {}'.format(s, text[max(s-x, 0):s-1],
                text[s:s+len(pattern)], text[s+len(pattern)+1: min(s+x, len(text))]))
                shift_pos.append(s)
            else:
                print('Spurious hit at s = {}, text = {}'.format(
                    s, text[s: s+window.m]))
                spurios_pos.append(s)

            window.shift_one()
    return shift_pos, spurios_pos

if __name__ == '__main__':
    text= '12345678910111213141516'
    pattern= '111'
    shift_pos, spurious_pos = rabin_karp(text, pattern)
    print('Shifts: {}, Spurious Hits: {}'.format(shift_pos, spurious_pos))
