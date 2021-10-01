"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, scale=1.0, null_zone=.01):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Hard Limiter',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.scale = scale
        self.null_zone = null_zone

    def work(self, input_items, output_items):
        output_items[0][:] = np.array(input_items[0] > self.null_zone, dtype=int) - np.array(-self.null_zone > input_items[0], dtype=int)
        return len(output_items[0])
