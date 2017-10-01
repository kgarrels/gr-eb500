#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr

import telnetlib



# TODO
# - expose cmd and udp ports as parameters
# - paramter for additional stream tags?
# - put borip_server.py and borip-EB500 stuff into examples
# - add message ports - which protocol?


class EB500Cmd (telnetlib.Telnet):
    def __init__(self, host=None, port=0):
        self = telnetlib.Telnet.__init__(self, host, port)
        print "EB500 connect to:", host, port

    def send_cmd(self, cmd):
        print "EB500< "+ cmd
        self.write(cmd+"\n")
        #ans = self.read_eager()     # FIXME: does not receive anything
        #print "< " + ans
        #return ans



class EB500Control(gr.basic_block):
    """
    docstring for block control
    """
    EB500_ADDR = '192.168.2.5'
    LOCALHOST = '127.0.0.1'
    CMD_PORT = 5555
    UDP_PORT = 28888
    
    def __init__(self, center_freq=14200000, sample_rate=640000, address = EB500_ADDR, port = CMD_PORT ):
        gr.basic_block.__init__(self, name="control", in_sig=None, out_sig=None)
        self.center_freq = center_freq
        self.sample_rate = sample_rate
        self.eb500d = EB500Cmd(address, port)
        
        self.eb500d.send_cmd('TRAC:UDP:DEL ALL')
        self.set_center_freq(center_freq)
        self.set_sample_rate(sample_rate)
        self.eb500d.send_cmd('SYST:IF:REM:MODE SHORT')
        self.eb500d.send_cmd('SYST:COMM:LAN:PING 0')
        self.eb500d.send_cmd('TRAC:UDP:TAG \"192.168.1.32\", ' + str(19000) + ',IF')
        
    def set_center_freq(self, freq):
        cmd = "freq " + str(freq)
        self.eb500d.send_cmd(cmd)

    def sampRate_to_bandWidth(self, samp):
        switcher = {
            320000: 250000,
            640000: 500000,
            1280000: 1000000,
            3200000: 2000000,
            6400000: 5000000
        }
        return switcher.get(samp)

    def set_sample_rate(self, sample_rate):
        bandwidth = self.sampRate_to_bandWidth(sample_rate)
        cmd = "band " + str(bandwidth)
        print "set bw " + str(bandwidth) + " from sr " + str(sample_rate)
        self.eb500d.send_cmd('TRAC:UDP:DEL ALL')
        self.eb500d.send_cmd(cmd)
        self.eb500d.send_cmd('TRAC:UDP:TAG \"192.168.1.32\", ' + str(19000) + ',IF')


    def general_work(self) :    #, input_items, output_items):
        #output_items[0][:] = input_items[0]
        #consume(0, len(input_items[0]))
        #self.consume_each(len(input_items[0]))
        return 0    #len(output_items[0])
