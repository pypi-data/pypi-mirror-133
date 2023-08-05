#!/usr/bin/python

import sys
import io
import unittest
import lmwsip
import lmwsip.tests.stubSipServer
import logging

from lmwsip.tests.stubSipServer import sipServer
from lmwsip.run import run
from datetime import datetime, timedelta
from dateutil import tz
from time import sleep

class myTestArgs():
    pass

class lmwsipTest(unittest.TestCase):

    def setUp(self):
        self.sipserver = sipServer()
        self.sip       = None
        self.sipserver.run()

    def login(self, **args):
        log = logging.basicConfig(level=logging.DEBUG)
        self.sip = lmwsip.LmwSip("USER", "PASS", "localhost",
                                  self.sipserver.port, ssl=False,
                                  log=log, **args)

    def tearDown(self):
        if self.sip:
            self.sip.closesocket()
        self.sipserver.kill()

    def test_sipobj(self):
        self.login()
        self.assertEqual(type(self.sip), lmwsip.LmwSip)

    def test_H1(self):
        self.sip = lmwsip.LmwSip(host=None)
        self.assertEqual(self.sip.period('H1'), 1)

    def test_H10(self):
        self.sip = lmwsip.LmwSip(host=None)
        self.assertEqual(self.sip.period('H10'), 10)

    def test_xHm0(self):
        self.sip = lmwsip.LmwSip(host=None)
        self.assertEqual(self.sip.period('xHm0'), 10)

    def test_Noparm(self):
        self.sip = lmwsip.LmwSip(host=None)
        with self.assertRaises(lmwsip.LmwParmWarn):
            self.assertEqual(self.sip.period('Noparm'), None)

    def test_loginfail(self):
        with self.assertRaises(lmwsip.LmwLoginFailure):
            self.sip = lmwsip.LmwSip("FAIL", "FAIL", "localhost",
                                      self.sipserver.port, ssl=False)

    def test_ti(self):
        self.login()
        self.assertEqual(type(self.sip.ti()), str)

    def test_telnetti(self):
        self.login(cleartelnet=True)
        self.assertEqual(type(self.sip.ti()), str)

    def test_cmd(self):
        self.login()
        self.assertEqual(type(self.sip.cmd("WN", "DUMMY", "H10", "+00:59", "2020-01-01", "00:00")), str)

    def test_cmderr(self):
        self.login()
        with self.assertRaises(lmwsip.LmwCmdWarn):
            self.assertEqual(type(self.sip.cmd("NOP", "DUMMY", "H10", "+00:59", "2020-01-01", "00:00")), str)

    def test_value(self):
        self.login()
        self.assertEqual(type(self.sip.value("WN", "DUMMY", "H10")), str)

    def test_value1min(self):
        self.login()
        self.assertEqual(type(self.sip.value("WN", "DUMMY", "H1")), str)

    def test_valueStr(self):
        self.login()
        self.assertEqual(type(self.sip.valueStr("WN", "DUMMY", "H10")), str)

    def test_logout(self):
        self.login()
        self.assertEqual(self.sip.logout(), None)

    def test_lmwTimeSerie(self):
        self.login()
        timezone = tz.gettz('GMT+1')
        res = self.sip.timeSerie("WN", "DUMMY", "H10",
                                  datetime.now(timezone)-timedelta(minutes=60),
                                  datetime.now(timezone))
        self.assertEqual(type(res.ts), list)
        self.assertEqual(len(res.ts), 6)
        self.assertEqual(res.ts[1][1][0], '1')

    def test_roundtime(self):
        self.login()
        timezone = tz.gettz('GMT+1')
        t1 = datetime(2020, 1, 1, 0, 10, 0, 0, timezone)
        t2 = datetime(2020, 1, 1, 0,  0, 0, 1, timezone)
        self.assertEqual(self.sip._roundtime_(t1, timedelta(minutes=10)), t1)
        self.assertEqual(self.sip._roundtime_(t2, timedelta(minutes=10)), t1)

    def test_closerecv(self):
        self.login()
        self.sip.send("CLOSE")
        with self.assertRaises(lmwsip.LmwSipConnectError):
            self.sip.recv()

    def test_closeti(self):
        self.login()
        self.sip.send("CLOSE")
        self.assertEqual(type(self.sip.ti()), str)

    def test_closecmd(self):
        self.login()
        self.sip.send("CLOSE")
        self.assertEqual(type(self.sip.cmd("WN", "DUMMY", "H10", "+00:59", "2020-01-01", "00:00")), str)

    def test_reconnect(self):
        self.login(reconnecttime=1)
        sleep(2)
        self.assertEqual(self.sip.sendrecv("LOGOUTCOUNT"), "1\r")

    def test_idlereconnect(self):
        self.login(idlereconnect=1)
        sleep(2)
        self.assertEqual(self.sip.sendrecv("LOGOUTCOUNT"), "1\r")

    def test_versionstr(self):
        self.assertEqual(type(lmwsip.__version__), str)

    def test_run(self):
        capturedOutput   = io.StringIO() 
        sys.stdout       = capturedOutput
        testSipFile      = io.StringIO("LI USER,PASS\rTI LMW\rLO")
        testSipFile.seek(0)
        args = myTestArgs()
        args.debug       = "DEBUG"
        args.host        = "localhost"
        args.port        = self.sipserver.port
        args.unencrypted = True
        args.acceptssl   = True
        args.cleartelnet = False
        args.time        = "+00:59"
        args.date        = "2020-01-01"
        args.files       = [testSipFile]
        run(args)
        args.files[0].close()
        self.assertEqual(capturedOutput.getvalue().find("!")>= 0, True)
        self.assertEqual(capturedOutput.getvalue().find("?"), -1)

if __name__ == '__main__':
    unittest.main()
