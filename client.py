# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time,socket,json
class Client():

    def __init__( self ):
        pass

    def connectshell( self ):

        data = {}
        data['Type'] = 3
        data['Body'] = { 'shell' : 'ping 127.0.0.1' }
        data = json.dumps( data )
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect(('10.1.1.13', 838))
        sock.send( data )

        print sock.recv(1024)  
        sock.close()  

if __name__=="__main__":
    clients = Client()
    clients.connectshell()