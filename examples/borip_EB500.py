#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Borip Eb500
# Generated: Mon Oct  2 11:53:49 2017
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import baz
import eb200
import eb500


class borip_EB500(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Borip Eb500")

        ##################################################
        # Variables
        ##################################################
        self.udp_port = udp_port = 19855
        self.samp_rate = samp_rate = 640000
        self.freq = freq = 14200000

        ##################################################
        # Blocks
        ##################################################
        self.sink = baz.udp_sink(gr.sizeof_short*1, '127.0.0.1', 28888, 1472, False, True)
        self.eb500_control_0 = eb500.EB500Control(freq, samp_rate, 'eb500', udp_port)
        self.eb200_if_stream_decode_0 = eb200.if_stream_decode(False)
        self.blocks_udp = blocks.udp_source(gr.sizeof_char*1, '192.168.1.32', udp_port, 32796, False)
        self.blocks_complex_to_interleaved_short_0 = blocks.complex_to_interleaved_short(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_interleaved_short_0, 0), (self.sink, 0))
        self.connect((self.blocks_udp, 0), (self.eb200_if_stream_decode_0, 0))
        self.connect((self.eb200_if_stream_decode_0, 0), (self.blocks_complex_to_interleaved_short_0, 0))

    def get_udp_port(self):
        return self.udp_port

    def set_udp_port(self, udp_port):
        self.udp_port = udp_port

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.eb500_control_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.eb500_control_0.set_center_freq(self.freq)


def main(top_block_cls=borip_EB500, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
