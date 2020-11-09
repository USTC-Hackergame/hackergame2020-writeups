#! /usr/bin/env python3
import subprocess
import tempfile
from netfilterqueue import NetfilterQueue
from scapy.all import *


### Config ###
#Editor to use (must be in path)

# Create a temporary file with the content and open the editor
# Proccess intercepted packets
def interrupt_and_edit_in(pkt):
	print("in")
	packet = IP(pkt.get_payload())
	packet[TCP].sport = 80
	del packet[IP].chksum
	del packet[TCP].chksum
	print(repr(packet))
	pkt.set_payload(raw(packet))
	pkt.accept()

if __name__=="__main__":

	nfqueue = NetfilterQueue()

	#Bind to the same queue number (here 2)
	nfqueue.bind(2, interrupt_and_edit_in)
	
	#run (indefinetely)
	try:
		nfqueue.run()
	except KeyboardInterrupt:
		print('Quiting...')
	nfqueue.unbind()
