"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, scale=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='HB FM Detect',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.scale = scale
        self.prev_last_i = 0
        self.prev_pent_i = 0
        self.prev_last_q = 0
        self.prev_pent_q = 0
        self.prev_last_theta = 0

    def work(self, input_items, output_items):
        i = input_items[0].real
        q = input_items[0].imag

        di = np.zeros(i.size)
        dq = np.zeros(q.size)

        dtheta = np.zeros(i.size)

        if i.size > 1:
            di[0] = i[0] - self.prev_pent_i
            di[1] = i[1] - self.prev_last_i
            dq[0] = q[0] - self.prev_pent_q
            dq[1] = q[1] - self.prev_last_q

            di[2:] = i[2:] - i[:-2]
            dq[2:] = q[2:] - q[:-2]

            dtheta[0] = self.scale*(self.prev_last_i*dq[0] - self.prev_last_q*di[0])
            dtheta[1:] = self.scale*(i[:-1]*dq[1:] - q[:-1]*di[1:])

            self.prev_last_i = i[-1]
            self.prev_pent_i = i[-2]
            self.prev_last_q = q[-1]
            self.prev_pent_q = q[-2]

        # theta = np.arctan2(q, i)
        # dtheta = np.zeros(theta.size)

        # dtheta[0] = theta[0] - self.prev_last_theta
        # dtheta[1:] = theta[1:] - theta[:-1]

        # dtheta[dtheta >= np.pi] -= 2*np.pi
        # dtheta[dtheta <= -np.pi] += 2*np.pi


        output_items[0][:] = dtheta

        #self.prev_last_theta = theta[-1]

        return len(output_items[0])
