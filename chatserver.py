import asyncore
import socket
from block import block

everyone = {}

class ChatHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            data = block(data)
            name = everyone[self.socket]
            if name is None:
                    everyone[self.socket]=data.strip()
                    return
            #print("read %d bytes" % len(data))
            for sock,name in everyone.items():
                sock.send(str(name)+': '+data)
        else:
           
            self.handle_close()

    def handle_close(self):
        if self.socket in everyone:
            print("Disconnect from %s" % repr(self.socket.getpeername()))
            #delete everyone socket

class ChatServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            sock.send("please log in\n'")
            everyone[sock]=None
            print 'Incoming connection from %s' % repr(addr)
            handler = ChatHandler(sock)
        
server = ChatServer('', 1776)
asyncore.loop()
