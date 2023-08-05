#!/usr/bin/python

"""A stub sipserver for testing lmwsip

This is a stub sipserver that implements a small subset of the sip
protocol to perform unit tests.

Implements the following commands:

  CMD> LI USER,PASS
  ANS< !

  CMD> TI LMW
  ANS< ! 20-JAN-01 00:00:00

  CMD> WN LMW,DUMMY,H10,+HH:MM,yyyy-mm-dd,HH:MM,DATA
  ANS< ! 1/10,;2/10;....

  CMD> WN LMW,DUMMY,H10,+HH:MM,yyyy-mm-dd,HH:MM,DATB
  ANS< ! 1/10/0;2/10/0;....

  CMD> WN LMW,DUMMY,H1,+HH:MM,yyyy-mm-dd,HH:MM,DATA
  ANS< ! 1/10,;2/10;....

  CMD> LO
  ANS< !

All other commands result in a "?"

  CMD> *
  ANS< ? ERROR

Note:
   for a WN command the time and date are ignored.
   The duration is used to calculare the number of results to send.

   The sip syntax for time is much flexibler.
   The stub only support this format!
"""


import os
import time
import random
import socketserver

logoutcount=0

class sipProtocol(socketserver.BaseRequestHandler):
    def match(self, m):
        return(self.data.find(m.encode()) == 0)
        
    def send(self, a):
        a = "%s\r" % a
        self.request.sendall(a.encode())

    def read(self):
        try:
            self.data = self.request.recv(1024).strip()
        except:
            self.data = None

    def number(self, b):
       if b[0] == b'0':
           return(int(b[0:1]))
       else:
           return(int(b[0:2]))

    def meting(self, delta=10):
        res  = ""
        sep  = "! "
        elem = self.data.decode().split(",") 
        h = self.number(elem[3][1:3])
        m = self.number(elem[3][4:6])
        aantal = 1+(60*h+m)//delta
        if self.data[-1:] == b'A':
            data = "%i/10"
        else:
            data = "%i/10/0"
        for i in range(aantal):
            res += sep+data % i
            sep=";"
        self.send(res)

    def handle(self):
        global logoutcount
        self.read()
        while self.data:
            if self.match("LI USER,PASS"):
                self.send("!")
            elif self.match("TI LMW"):
                self.send("! 20-JAN-01 00:00:00")
            elif self.match("WN LMW,DUMMY,H10,"):
                self.meting(10)
            elif self.match("WN LMW,DUMMY,H1,"):
                self.meting(1)
            elif self.match("LOGOUTCOUNT"):
                self.send(str(logoutcount))
            elif self.match("LO"):
                logoutcount+=1
                self.send("!")
            elif self.match("CLOSE"):
                self.request.close()
            else:
                self.send("? ERROR")
            self.read()
              
class sipServer(socketserver.TCPServer):
    def __init__(self):
        self.port = None
        while self.port == None:
            self.port = random.randint(20000, 50000)
            try:
                super(sipServer, self).__init__(("localhost", self.port), sipProtocol)
            except:
                self.port = None

    def run(self):
        self.pid = os.fork()
        if self.pid == 0:
            self.serve_forever()

    def kill(self):
        if self.pid != 0:
            os.kill(self.pid, 15)
        self.server_close()

if __name__ == '__main__':
    s = sipServer()
    s.run()
    pass
