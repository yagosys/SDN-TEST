#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def emptyNet():

    NODE1_IP='<%= @hosts['opendaylight-mininet-1']['ipaddress'] %>'
    CONTROLLER_IP='127.0.0.1'

    net = Mininet( topo=None,
                   build=False)

    net.addController( 'c1',
                      controller=RemoteController,
                      ip=CONTROLLER_IP,
                      port=6633)

    h6 = net.addHost( 'h6', ip='10.0.0.6' )

    s4 = net.addSwitch( 's4' )
    s5 = net.addSwitch( 's5' )
    s6 = net.addSwitch( 's6' )

    net.addLink( s4, s6 )
    net.addLink( s4, s5 )

    net.addLink( h6, s5 )

    net.start()

    # Configure the GRE tunnel
    s4.cmd('ovs-vsctl add-port s4 s4-eth3 -- set interface s4-eth3 type=gre options:remote_ip='+NODE1_IP)
    s4.cmdPrint('ovs-vsctl show')

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()
