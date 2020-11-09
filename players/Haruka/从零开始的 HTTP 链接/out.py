#! /usr/bin/env python3
import subprocess
import tempfile
from netfilterqueue import NetfilterQueue
from scapy.all import *


### Config ###
#Editor to use (must be in path)

# Create a temporary file with the content and open the editor
# Proccess intercepted packets
def interrupt_and_edit_out(pkt):
	print("out")
	packet = IP(pkt.get_payload())
	packet[TCP].dport = 0
	del packet[IP].chksum
	del packet[TCP].chksum
	print(repr(packet))
	pkt.set_payload(raw(packet))
	pkt.accept()

if __name__=="__main__":

	nfqueue = NetfilterQueue()

	#Bind to the same queue number (here 2)
	nfqueue.bind(3, interrupt_and_edit_out)
	
	#run (indefinetely)
	try:
		nfqueue.run()
	except KeyboardInterrupt:
		print('Quiting...')
	nfqueue.unbind()
