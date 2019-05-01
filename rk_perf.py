import matplotlib.pyplot as plt
import rabin_karp as rk
import time
import random

# Plot graphs


def plot_graph(data, title, x, y, data2=None, legend=None):
    z = list(zip(*data))
    plt.plot(z[0], z[1])
    if data2:
        q = list(zip(*data2))
        plt.plot(q[0], q[1])
        if legend:
            plt.legend(legend)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()


filename = 'big.txt'
text = ''
pattern = ''
with open(filename) as f:
    for l in f.readlines():
        text += l
    f.close()
print('Total Length of Text: {}'.format(len(text)))
pattern_pos = random.randint(0, len(text) - 5000)
pattern = text[pattern_pos:pattern_pos+5000]
print('Total Length of Pattern: {}'.format(len(pattern)))

# Vary length of text, pattern is fixed
short_pattern = pattern[:1000]
short_text = text[:200000]
print('Length of Short Pattern: {}, Short Text: {}'.format(
    len(short_pattern), len(short_text)))
time_text = []
pr = rk.get_rand(32)
for i in [200, 300, 500, 1000, 5000, 10000, 50000, 100000, 200000]:
    start = time.time()
    rk.rabin_karp(text[:i+1], short_pattern[:min(1000, i)], prime=pr, radix=13)
    end = time.time()
    time_text.append((i, end-start))


# Vary length of pattern, text is fixed
time_p = []
for i in [1, 5, 10, 20, 50, 100, 250, 500, 1000, 2000, 5000]:
    start = time.time()
    rk.rabin_karp(short_text, pattern[:i+1], prime=pr)
    end = time.time()
    time_p.append((i, end-start))

# Vary Radix
time_r = []
for i in [128, 140, 150, 175, 200, 225, 256]:
    start = time.time()
    rk.rabin_karp(short_text, short_pattern, radix=i, prime=pr)
    end = time.time()
    time_r.append((i, end-start))


def naive_match(t, p):
    for x in range(len(t) - len(p)):
        z = 0
        for y in range(len(p)):
            if not p[y] == t[x+y]:
                break
            z += 1
        if z == len(p):
            pass


# Compare Naive with RK with lenght of text
time_c_t_n = []
for i in [200, 300, 500, 1000, 5000, 10000, 50000, 100000, 200000]:
    start = time.time()
    # rk.verify_shifts(text[:i], short_pattern[:min(i, 1000)], [])
    t = text[:i]
    p = short_pattern[:min(i, 1000)]

    naive_match(t, p)

    end = time.time()
    time_c_t_n.append((i, end-start))

time_c_p_n = []
for i in [1, 5, 10, 20, 50, 100, 250, 500, 1000, 2000, 5000]:
    start = time.time()
    t = short_text
    p = pattern[:i]
    # rk.verify_shifts(short_text, pattern[:i], [])
    naive_match(t, p)
    end = time.time()
    time_c_p_n.append((i, end-start))

plot_graph(time_text, 'Performance of Rabin-Karp over Varying Text Size',
           'Lenght of Text', 'Time (s)')
plot_graph(time_p, 'Performance of Rabin-Karp over Varying Pattern Size',
           'Lenght of Pattern', 'Time (s)')
plot_graph(time_r, 'Performance of Rabin-Karp over Varying Radix Size',
           'Radix', 'Time (s)')
plot_graph(time_c_t_n, 'Performance of Rabin-Karp vs Naive String Matching over Varying Text Size',
           'Lenght of Text', 'Time (s)', time_text, ['Naive String Matcher', 'Rabin Karp'])
plot_graph(time_c_p_n, 'Performance of Rabin-Karp vs Naive String Matching over Varying Pattern Size',
           'Lenght of Text', 'Time (s)', time_p, ['Naive String Matcher', 'Rabin Karp'])
