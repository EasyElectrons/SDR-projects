"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.interp_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, scale=1.0, sps=25):  # only default arguments here
        gr.interp_block.__init__(
            self,
            name='Unipolar NRZ Encoder',   # will show up in GRC
            in_sig=[np.int8],
            out_sig=[np.float32],
            interp=sps
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.scale = scale
        self.sps = sps

    def work(self, input_items, output_items):
        output_items[0][:] = np.kron(input_items[0], np.ones(self.sps))*self.scale
        return len(output_items[0])
