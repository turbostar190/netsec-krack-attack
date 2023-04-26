#!/usr/bin/env python

"""This code tests if APs are affected by CVE-2017-13082 (KRACK attack) and
determine whether an implementation is vulnerable to attacks on FT protocol 802.11r."""

__author__ = "Ramon Fontes and 2022/2023 Group4"
__credits__ = ["https://github.com/vanhoefm/krackattacks-test-ap-ft"]

from time import sleep

from mininet.log import setLogLevel, info
from mininet.term import makeTerm
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
import os


def topology():

    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', ip='10.0.0.1/8', position='50,0,0',
                          encrypt='wpa2')
    # sta1.set_circle_color('r')
    ap1 = net.addStation('ap1', mac='02:00:00:00:01:00',
                         ip='10.0.0.101/8', position='10,30,0')
    # ap1.set_circle_color('b')
    ap2 = net.addStation('ap2', mac='02:00:00:00:02:00',
                         ip='10.0.0.102/8', position='100,30,0')
    # ap2.set_circle_color('g')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", sL=0.4, exp=3.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Linking nodes\n")
    net.addLink(ap1, ap2)

    info("*** Configuring AP settings\n")
    # Configuration of access point 1 and 2
    # Master is the mode acting as an access point
    ap1.setMasterMode(intf='ap1-wlan0', ssid='handover', channel='1',
                      ieee80211r=True, mobility_domain='a1b2',
                      passwd='123456789a', encrypt='wpa2', datapath="user")
    ap2.setMasterMode(intf='ap2-wlan0', ssid='handover', channel='6',
                      ieee80211r=True, mobility_domain='a1b2',
                      passwd='123456789a', encrypt='wpa2', datapath="user")

    info("*** Plotting Graph\n")
    net.plotGraph(min_x=-100, min_y=-100, max_x=200, max_y=200)

    info("*** Starting network\n")
    net.build()

    # Monitor mode, or RFMON (Radio Frequency MONitor) mode, allows a computer with a wireless network 
    # interface controller (WNIC) to monitor all traffic received on a wireless channel
    sta1.cmd("iw dev sta1-wlan0 interface add mon0 type monitor")
    sta1.cmd("ifconfig mon0 up")

    sleep(5)
    # We need AP scanning. Otherwise, roam won't work
    makeTerm(sta1, title='Scanning', cmd="bash -c 'echo \"AP Scanning\" && iw dev sta1-wlan0 scan; read;'")
    # Initialize the FT test monitor
    sleep(15)
    sta1.cmd("killall wpa_supplicant")
    makeTerm(sta1, title='KrackAttack', cmd="bash -c 'cd krackattacks-scripts/krackattack && source venv/bin/activate && python krack-ft-test.py wpa_supplicant -D nl80211 -i sta1-wlan0 -c ../../sta1-wlan0_0.staconf;'")
    makeTerm(sta1, title='wpa_cli')

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()

