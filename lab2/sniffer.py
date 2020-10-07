import sys

# if len(sys.argv) != 3:
#     print "Usage: ",sys.argv[0],"  "
#     sys.exit(1)
# ipa=sys.argv[1]
# iface=sys.argv[2]
#
# def psv_output(pkt):
#     if pkt.haslayer(IP):
#        return pkt.command()
#
# def myfilter(pkt):
#     if pkt.haslayer(IP):
#        return ((pkt[IP].dst == ipa) or (pkt[IP].src == ipa))
#
# sniff(prn=psv_output, iface=iface, lfilter=myfilter, store=0)
from scapy.sendrecv import sniff

if __name__ == '__main__':
    packets = sniff()
    packets.summary()
