import numpy as np
from numpy import random
from Crypto.Util import number
import sys

keypair_prefix = 'keypair'
def_num_entries = 100


def get_rand_prime(nbits):
    return number.getPrime(nbits)


def get_rand_num(digits=19):
    tmp = ''
    for _ in range(digits):
        if not tmp:
            # No 0 as starting digit
            tmp += str(random.randint(1, 10))
        else:
            tmp += str(random.randint(0, 10))

    return int(tmp)


def gen_data(outfile, num_entries):
    with open(outfile, 'w') as f:
        for _ in range(num_entries):
            f.write('{}\n'.format(get_rand_num()))
    f.close()


def gen_key_pair(nbits=64):
    p = get_rand_prime(nbits)
    q = get_rand_prime(nbits)

    n = p*q
    phi = (p-1)*(q-1)

    e = np.int64(0)
    while(not number.GCD(e, phi) == 1):
        e = random.randint(3, 2**31)

    d = number.inverse(e, phi)
    print('Public Key: {}'.format((e, n)))
    print('Private Key: {}'.format((d, n)))

    return (e, n), (d, n)


def load_keys(filenameprefix=keypair_prefix):
    pkey = '{}_public.key'.format(filenameprefix)
    skey = '{}_private.key'.format(filenameprefix)

    e, n, d = 0, 0, 0
    with open(pkey) as f:
        l = f.readline().split(',')
        e = int(l[0].strip())
        n = int(l[1].strip())
        f.close()

    with open(skey) as f:
        l = f.readline().split(',')
        d = int(l[0].strip())
        f.close()

    return (e, n), (d, n)


def encrypt_num(ch, key_pair):
    return pow(ch, key_pair[0], key_pair[1])


def decrypt_num(ch, key_pair):
    return pow(ch, key_pair[0], key_pair[1])


def encrypt_file(filename, outfile, keyprefix=keypair_prefix, num_entries=def_num_entries):
    pkey = '{}_public.key'.format(keypair_prefix)
    skey = '{}_private.key'.format(keypair_prefix)

    print('Encrypting file {} using Key from files {}, {}'.format(
        filename, pkey, skey))
    (e, n), (d, n) = load_keys(keypair_prefix)
    out = open(outfile, 'w')
    with open(filename) as f:
        i = 0
        lines = f.readlines()
        for i in range(min(num_entries, len(lines))):
            try:
                out.write('{}\n'.format(encrypt_num(
                    int(lines[i].strip()), (e, n))))
            except:
                print(
                    '{} is not a number, this entry will be skipped'.format(lines[i]))
        f.close()
    out.close()


def decrypt_file(filename, outfile, keyprefix=keypair_prefix):
    pkey = '{}_public.key'.format(filename)
    skey = '{}_private.key'.format(filename)

    print('Encrypting file {} using Key from files {}, {}'.format(
        filename, pkey, skey))
    (e, n), (d, n) = load_keys(keypair_prefix)
    out = open(outfile, 'w')
    with open(filename) as f:
        for l in f.readlines():
            out.write('{}\n'.format(decrypt_num(int(l.strip()), (d, n))))
        f.close()
    out.close()


def gen_and_save_key_pair(keyprefix, nbits):
    pkey = '{}_public.key'.format(keyprefix)
    skey = '{}_private.key'.format(keyprefix)

    print('Saving keypair to "{}, {}"'.format(pkey, skey))
    (e, n), (d, n) = gen_key_pair(nbits=nbits)

    with open(pkey, 'w') as f:
        f.write('{},{}'.format(e, n))
        f.close()

    with open(skey, 'w') as f:
        f.write('{},{}'.format(d, n))
        f.close()


def rsa():
    (e, n), (d, n) = gen_key_pair()
    C = encrypt_num(50384578240926184261153170855015391643, (e, n))
    P = decrypt_num(C, (d, n))

    print(C, P)


if __name__ == '__main__':
    args = sys.argv
    arglen = len(args)

    # rsa()
    if arglen <= 1:
        print('Usage: {} {}'.format(args[0], 'genkey|encrypt|decrypt|gendata'))
        exit()

    if args[1].lower() == 'genkey':
        filename = keypair_prefix
        nbits = 64
        if arglen >= 3:
            filename = args[2]
        if arglen >= 4:
            nbits = args[3]

        gen_and_save_key_pair(filename, nbits)

    elif args[1].lower() == 'encrypt':
        if arglen < 4:
            print('Usage: {} {} {} {}'.format(
                args[1], '<filename to encrypt>', '<outfile>', '[<keypair file prefix>]'))
            exit()

        keyfile = keypair_prefix
        if arglen >= 5:
            keyfile = args[4]

        outfile = args[3]
        filename = args[2]

        encrypt_file(filename, outfile, keyfile)

    elif args[1].lower() == 'decrypt':
        if arglen < 4:
            print('Usage: {} {} {}'.format(
                args[1], '<encrypted file>', '<out file>'  '[<keypair file prefix>]'))
            exit()

        keyfile = keypair_prefix
        if arglen >= 5:
            keyfile = args[4]

        outfile = args[3]
        filename = args[2]
        decrypt_file(filename, outfile, keyfile)
    elif args[1].lower() == 'gendata':
        outfile = 'data.txt'
        num_entries = 100
        if arglen < 3:
            print('Usage: {} {} {}'.format(
                args[1], '<Out file>', '[<Num Entries>]'))
            exit()

        if arglen == 4:
            num_entries = args[3]

        outfile = args[2]
        gen_data(outfile, num_entries)
    else:
        print('Usage: {} {}'.format(args[0], 'genkey|encrypt|decrypt'))
