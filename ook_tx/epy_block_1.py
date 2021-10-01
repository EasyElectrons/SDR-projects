"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, samp_rate=30e3, baud=1200):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Gaussian Filter - py',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.sigma = samp_rate/(2*np.pi*baud)
        self.N = int(np.ceil(6*self.sigma - 1) // 2 * 2 + 1) # force up to next odd integer
        x = np.linspace(-5*self.sigma, 5*self.sigma, self.N)
        self.g = 1/np.sqrt(2*np.pi*self.sigma**2) * np.exp(-x**2/(2*self.sigma**2))
        #print('Generated gaussian kernel with N = ' + str(self.N))
        self.last_buf = np.zeros(self.N-1)

    def work(self, input_items, output_items):
        work_conv = np.concatenate((self.last_buf, input_items[0]))

        # for i in range(0, output_items[0].size):
        #     s = 0

        #     for j in range(0, self.g.size):
        #         s += work_conv[i-j+self.N-1] * self.g[j]

        #     output_items[0][i] = s

        output_items[0][:] = np.convolve(work_conv, self.g, 'valid')

        self.last_buf = input_items[0][-(self.N-1):]

        return len(output_items[0])
