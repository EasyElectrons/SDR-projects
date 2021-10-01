import bitstring as bs
import numpy as np
import matplotlib.pyplot as plt
import sys
np.set_printoptions(threshold=sys.maxsize)

f_tx = open('unpacked.tx.8u.real')
f_rx = open('unpacked.rx.8u.real')

file_bits_tx = bs.BitArray(f_tx)
file_bits_rx = bs.BitArray(f_rx)

pyld_bits_tx = []
pyld_bits_rx = []

p = 0
for i in range(0, file_bits_tx.length, 8):
	pyld_bits_tx.append((file_bits_tx[i:i+8].bytes)[-1])
	p += 1

p = 0
for i in range(0, file_bits_rx.length, 8):
	pyld_bits_rx.append((file_bits_rx[i:i+8].bytes)[-1])
	p += 1

usable_len = min((len(pyld_bits_tx), len(pyld_bits_rx)))

pyld_bits_tx = np.array(pyld_bits_tx[0:usable_len])
pyld_bits_rx = np.array(pyld_bits_rx[0:usable_len])

sums_abs_diff = []

for i in range(0, 8):
	if i == 0:
		diff = pyld_bits_tx - pyld_bits_rx
	else:
		diff = pyld_bits_tx[:-i] - pyld_bits_rx[i:]

	abs_diff = np.abs(diff)
	sums_abs_diff.append(np.sum(abs_diff))

sum_abs_diff = min(sums_abs_diff)

ber = sum_abs_diff/usable_len

print(sums_abs_diff)
print('ratio = ' + str(sum_abs_diff) + ' / ' + str(usable_len))
print('ber = ' + str(ber))
