"""
Simple Topology

    client --- switch0 --- switch1 ... --- switch19 --- server

"""
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI


class CustomTopo(Topo):

    BANDWIDTH = 10  # Mbps
    LOSS = 0.1  # 2% loss
    DELAY = "5ms"  # 5ms delay
    LINK_OPTS = {"bw": BANDWIDTH, "delay": DELAY, "loss": LOSS, "cls": TCLink}

    def build(self, n=10):
        clientHost = self.addHost("client")
        serverHost = self.addHost("server")
        switchList = []
        for i in range(n):
            switch = self.addSwitch("s" + str(i))
            switchList.append(switch)

        self.addLink(clientHost, switchList[0], **self.LINK_OPTS)
        for i in range(0, n - 1):
            self.addLink(switchList[i], switchList[i + 1], **self.LINK_OPTS)
        self.addLink(switchList[n - 1], serverHost, **self.LINK_OPTS)


topos = {"customtopo": CustomTopo}


def simpleTest():
    topo = CustomTopo(n=10)
    net = Mininet(topo)
    net.start()
    print("Pinging from client to server")
    client = net.get("client")
    server = net.get("server")
    server.cmd("python server/server.py 80 &")
    time.sleep(2)
    # TODO
    # client.cmd(f"run benchmark script {server.IP()}")
    CLI(net)
    net.stop()


if __name__ == "__main__":
    simpleTest()
