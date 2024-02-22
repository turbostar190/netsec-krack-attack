#!/usr/bin/env python

"""This code tests if APs are affected by CVE-2017-13082 (KRACK attack) and
determine whether an implementation is vulnerable to attacks on FT protocol 802.11r
in a Mininet-wifi environment."""

__author__ = "Ramon Fontes and UNITN 2022/2023 Network Security master course Group14 Lab"
__credits__ = ["https://github.com/vanhoefm/krackattacks-scripts"]

from time import sleep
import subprocess
import os

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
    sta1 = net.addStation('sta1', ip='10.0.0.1/8', position='50,0,0',
                          encrypt='wpa2')    

    info("*** Configuring AP settings\n")
    # Configuration of access point 1 and 2
    ap1 = net.addAccessPoint('ap1',  mac='02:00:00:00:01:00', ssid="handover", mode="g", 
                             channel="1", ieee80211r='yes', mobility_domain='a1b2', 
                             passwd='123456789a', encrypt='wpa2', position='10,30,0', 
                             inNamespace=True, datapath="user", failMode="standalone")
    ap2 = net.addAccessPoint('ap2', mac='02:00:00:00:02:00', ssid="handover", mode="g", 
                             channel="6", ieee80211r='yes', mobility_domain='a1b2', 
                             passwd='123456789a', encrypt='wpa2', position='100,30,0', 
                             inNamespace=True, datapath="user", failMode="standalone")

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", sL=0.4, exp=3.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Linking nodes\n")
    net.addLink(ap1, ap2)

    info("*** Plotting Graph\n")
    net.plotGraph(min_x=-100, min_y=-100, max_x=200, max_y=200)

    info("*** Starting network\n")
    net.build()
    ap1.cmd('ifconfig ap1-wlan1 10.0.0.101/8')
    ap2.cmd('ifconfig ap2-wlan1 10.0.0.102/8')
    os.system('ip link set hwsim0 up')


    # Monitor mode, or RFMON (Radio Frequency MONitor) mode, allows a computer with a wireless network 
    # interface controller (WNIC) to monitor all traffic received on a wireless channel
    sta1.cmd("iw dev sta1-wlan0 interface add mon0 type monitor")
    sta1.cmd("ifconfig mon0 up")

    # print hostapd version (hostapd by default outputs on stderr???)
    hostapd = subprocess.Popen(["hostapd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        output = subprocess.check_output(("grep", "v[0-9].[0-9]*"), stdin=hostapd.stderr)
    except: 
        output = subprocess.check_output(("grep", "v[0-9].[0-9]*"), stdin=hostapd.stdout)
    hostapd.wait()
    info("Using %s" % output)
    # print kernel version
    kernel = subprocess.check_output(("uname", "-r"))
    info("Using kernel v%s\n" % kernel)

    # start wireshark
    sta1.cmd("wireshark &")

    sleep(5)

    # We need AP scanning. Otherwise, roam won't work
    makeTerm(sta1, title='Scanning', cmd="bash -c 'echo \"AP Scanning\" && wpa_cli -i sta1-wlan0 scan; read;'")

    sleep(15)

    # remove any previosly opened interfaces
    sta1.cmd("killall wpa_supplicant")
    # Initialize the FT test monitor
    makeTerm(sta1, title='KrackAttack', cmd="bash -c 'cd krackattacks-scripts/krackattack && source venv/bin/activate && python krack-ft-test.py wpa_supplicant -D nl80211 -i sta1-wlan0 -c ../../sta1-wlan0_0.staconf;'")
    makeTerm(sta1, title='wpa_cli')

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()

