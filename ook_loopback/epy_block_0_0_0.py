"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.decim_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, sps=25, symbol_threshold=.5):  # only default arguments here
        gr.decim_block.__init__(
            self,
            name='Clocked Unipolar NRZ Decoder',   # will show up in GRC
            in_sig=[np.float32, np.float32],
            out_sig=[np.int8],
            decim=sps
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.sps = sps
        self.sym_thresh = symbol_threshold

    def work(self, input_items, output_items):
        io = 0

        for n in range(1, input_items[0].size):
            if input_items[1][n-1] < -.01 and .01 < input_items[1][n]: #rising edge
                if io >= output_items[0].size:
                    output_items[0][:-1] = output_items[0][1:] # shift the first off the edge
                    io -= 1

                output_items[0][io] = int(input_items[0][n] > self.sym_thresh)
                io += 1

        return io
