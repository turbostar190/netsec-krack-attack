#!/usr/bin/env python

"""This code tests if a client is affected by CVE-2017-13077 and 
CVE-2017-13078 (KRACK attack) and determine whether an 
implementation is vulnerable to attacks in a Mininet-wifi environment."""

__author__ = "Ramon Fontes and UNITN 2022/2023 Network Security master course Group14 Lab"
__credits__ = ["https://github.com/vanhoefm/krackattacks-scripts"]

from time import sleep
import subprocess

from mininet.log import setLogLevel, info
from mininet.term import makeTerm
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference


def topology():

    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    ap1 = net.addStation('ap1', mac='02:00:00:00:01:00', position='10,30,0', inNamespace=True)
    sta1 = net.addStation('sta1', ip='192.168.100.100/24', position='50,0,0', inNamespace=True)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", sL=0.4, exp=3.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Plotting Graph\n")
    net.plotGraph(min_x=-100, min_y=-100, max_x=200, max_y=200)

    info("*** Starting network\n")
    net.build()


    # Monitor mode, or RFMON (Radio Frequency MONitor) mode, allows a computer with a wireless network 
    # interface controller (WNIC) to monitor all traffic received on a wireless channel
    ap1.cmd("iw dev ap1-wlan0 interface add mon0 type monitor")
    ap1.cmd("ifconfig mon0 up")
    sta1.cmd("iw dev sta1-wlan0 interface add mon0 type monitor")
    sta1.cmd("ifconfig mon0 up")
    
    # print wpa_supplicant version
    wpa_s = subprocess.Popen(["wpa_supplicant"], stdout=subprocess.PIPE)
    output = subprocess.check_output(("grep", "v[0-9].[0-9]*"), stdin=wpa_s.stdout)
    wpa_s.wait()
    info("Using %s\n" % output)

    sleep(10)

    # launch script listener script on the access point
    makeTerm(ap1, title='AP', cmd="bash -c 'cd krackattacks-scripts/krackattack && source venv/bin/activate && python krack-test-client.py;'")

    sleep(5)
    
    # remove any previosly opened interfaces
    sta1.cmd("killall wpa_supplicant")
    # connect the client to the AP
    makeTerm(sta1, title='Connection', cmd="bash -c 'wpa_supplicant -i sta1-wlan0 -c client-network.conf'")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()

