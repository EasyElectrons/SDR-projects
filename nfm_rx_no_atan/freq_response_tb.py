import numpy as np
import matplotlib.pyplot as plt
import pickle

def fm_det_no_atan(input_items, output_items):
    i = input_items.real
    q = input_items.imag

    di = np.zeros(i.size)
    dq = np.zeros(q.size)

    dtheta = np.zeros(i.size)

    if i.size > 1:

        di[2:] = i[2:] - i[:-2]
        dq[2:] = q[2:] - q[:-2]

        dtheta[1:] = i[:-1]*dq[1:] - q[:-1]*di[1:]
        dtheta = dtheta[1:] # make both det outputs the same size

        output_items[:] = dtheta

def fm_det_normal(input_items, output_items):
    i = input_items.real
    q = input_items.imag

    pha = np.arctan2(q, i)

    pha[pha > np.pi] -= 2*np.pi
    pha[pha < np.pi] += 2*np.pi

    freq = pha[1:] - pha[:-1]

    output_items[:] = freq

def pickle_data(fp_no_atan, fp_normal, fs, n, F_MIN, F_MAX, f, ampls_no_atan, ampls_normal):
    op_no_atan = np.zeros(n.size-1)
    op_normal = np.zeros(n.size-1)
    fia = 0

    for fi in range(F_MIN, F_MAX):
        print(fi)

        ip = np.exp(1j*2*np.pi*fi*n)

        fm_det_no_atan(ip, op_no_atan)
        fm_det_normal(ip, op_normal)

        ampls_no_atan[fia] = np.max(op_no_atan)
        ampls_normal[fia] = np.max(op_normal)
        fia += 1

    file_no_atan = open(fp_no_atan, 'wb')
    pickle.dump(ampls_no_atan, file_no_atan)
    file_no_atan.close()
    file_normal = open(fp_normal, 'wb')
    pickle.dump(ampls_normal, file_normal)
    file_no_atan.close()

fs = 30e3
n = np.linspace(0, 1, int(fs))
F_MIN = int(100) # inclusive
F_MAX = int(10e3) # exclusive
f = np.linspace(F_MIN, F_MAX - 1, F_MAX - F_MIN)
ampls_no_atan = np.zeros(f.size)
ampls_normal = np.zeros(f.size)

#pickle_data('ampls_no_atan.32f.real', 'ampls_normal.32f.real', fs, n, F_MIN, F_MAX, f, ampls_no_atan, ampls_normal)

file_no_atan = open('ampls_no_atan.32f.real', 'rb')
ampls_no_atan = pickle.load(file_no_atan)
file_no_atan.close()
file_normal = open('ampls_normal.32f.real', 'rb')
ampls_normal = pickle.load(file_normal)
file_normal.close()

deriv_no_atan = ampls_no_atan[1:] - ampls_no_atan[:-1]
deriv_normal = ampls_normal[1:] - ampls_normal[:-1]
conc_no_atan = deriv_no_atan[1:] - deriv_no_atan[:-1]
conc_normal = deriv_normal[1:] - deriv_normal[:-1]

db_no_atan = 20*np.log10(ampls_no_atan)
db_normal = 20*np.log10(ampls_normal)

plt.subplot(1, 2, 1)
plt.plot(f, db_no_atan)
plt.plot(f, db_normal)
plt.xscale('log')
plt.legend(['no atan', 'normal'])
plt.title('magnitude responses @ 30 kHz')
plt.xlabel('frequency (Hz)')
plt.ylabel('amplitude (dBV)')
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(f[2:], conc_no_atan)
plt.plot(f[2:], conc_normal)
plt.xscale('log')
plt.legend(['no atan', 'normal'])
plt.title('concavity of magnitude responses')
plt.xlabel('frequency (Hz)')
plt.ylabel('amplitude (V/V)')
plt.grid()

plt.show()

