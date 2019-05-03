import matplotlib.pyplot as plt
import rsa
import time

key_size = 64
infile = 'cc.txt'
outfile = 'cc_e.txt'
defile = 'cc_d.txt'
keyprefix = rsa.keypair_prefix

num_entries = 500
# Generate 10,000 keys to use
rsa.gen_data(infile, 10000)

# Measure performance of Algo with Key size
time_bits = []
for i in [16, 32, 48, 64, 96, 128]:
    rsa.gen_and_save_key_pair(keyprefix, i)
    start = time.time()
    rsa.encrypt_file(infile, outfile, num_entries=num_entries)
    rsa.decrypt_file(outfile, defile)
    end = time.time()
    time_bits.append((i, end-start))

rsa.gen_and_save_key_pair(keyprefix, key_size)
# Vary number of entries for fixed Key Size
time_entries = []
for i in [1, 5, 10, 100, 200, 500, 1000, 2000, 5000, 10000]:
    start = time.time()
    rsa.encrypt_file(infile, outfile, num_entries=i)
    rsa.decrypt_file(outfile, defile)
    end = time.time()
    time_entries.append((i, end-start))


# Vary length of number
time_num = []
rsa.gen_and_save_key_pair(keyprefix, nbits=128)
(e, n), (d, n) = rsa.load_keys(keyprefix)
for i in [x for x in range(1, 41)]:  # 2,4,6...40
    start = time.time()
    for _ in range(100):  # Repeat 100 times
        p = rsa.get_rand_num(digits=i)
        # print('{}'.format(p))
        c = rsa.encrypt_num(p, (e, n))
        rsa.decrypt_num(c, (d, n))
    end = time.time()
    time_num.append((i, end-start))


# Plot graphs
def plot_graph(data, title, x, y):
    z = list(zip(*data))
    plt.plot(z[0], z[1])
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()


plot_graph(time_bits, 'Varying number of bits in Key',
           'Number of Bits', 'Time (s)')
plot_graph(time_entries, 'Varying number of entries',
           'Number of Entries encrypted/decrypted', 'Time (s)')
plot_graph(time_num, 'Varying length of number encrypted',
           'Number of Digits', 'Time (s)')
