import unittest
from ipsecparse import loads, dumps, Key, Keys

class TestIpsecParse(unittest.TestCase):

    def setUp(self):
        # example configuration from https://wiki.strongswan.org/projects/strongswan/wiki/IpsecConf
        self.strongswan_in = """\
# /etc/ipsec.conf - strongSwan IPsec configuration file

config setup
    cachecrls=yes
    strictcrlpolicy=yes

ca strongswan  #define alternative CRL distribution point
    cacert=strongswanCert.pem
    crluri=http://crl2.strongswan.org/strongswan.crl
    auto=add

conn %default
    keyingtries=1
    keyexchange=ikev2

conn roadwarrior
    leftsubnet=10.1.0.0/16
    leftcert=moonCert.pem
    leftid=@moon.strongswan.org
    right=%any
    auto=add
"""

        self.strongswan_out = """\
config setup
    cachecrls=yes
    strictcrlpolicy=yes

ca strongswan
    cacert=strongswanCert.pem
    crluri=http://crl2.strongswan.org/strongswan.crl
    auto=add

conn %default
    keyingtries=1
    keyexchange=ikev2

conn roadwarrior
    leftsubnet=10.1.0.0/16
    leftcert=moonCert.pem
    leftid=@moon.strongswan.org
    right=%any
    auto=add
"""

 
    def test1(self):
        self.assertEqual(
            dumps(loads(self.strongswan_in), indent = '    '),
            self.strongswan_out
        )

   
    def test2_empty_lines(self):
        conf = """


config setup

    nat_traversal=yes
    
    
    strictcrlpolicy=yes

"""
        self.assertEqual(
            dumps(loads(conf), indent = '    '),
            """\
config setup
    nat_traversal=yes
    strictcrlpolicy=yes
"""
        )

        
    def test3_empty_values(self):
        conf = """
conn myconn1
    dpddelay=
    salifetime=1h
    aggrmode=

conn myconn2
    phase2=esp
    leftsubnet=
"""
        conf = loads(conf)
        self.assertEqual(conf['conn', 'myconn1']['dpddelay'], '')
        self.assertEqual(conf['conn', 'myconn1']['aggrmode'], '')
        self.assertEqual(conf['conn', 'myconn2']['leftsubnet'], '')

    
    def test4(self):
        conf = """
config setup
    nat_traversal=yes
    plutodebug="all crypt" # testing quoted string
    
conn myconn
    left=192.168.0.2
    right=10.0.0.1"""
        conf = loads(conf)
        self.assertEqual(conf['config','setup']['plutodebug'], "all crypt")


    def test5_conn_filter(self):
        conf = loads(self.strongswan_in)
        
        names = lambda lst: list(x[0] for x in lst)

        self.assertEqual(
            names(conf.conn_filter(
                Key('leftsubnet') == '10.1.0.0/16' and Key('right') == '%any'
            )),
            ['roadwarrior']
        )
        conf['conn', 'myconn'] = {'left': '10.1.0.1', 'right': '192.168.0.2'}
        
        self.assertEqual(
            names(conf.conn_filter(
                Keys('left', 'right').contains('192.168.0.2')
            )),
            ['myconn']
        )
        
        self.assertEqual(
            names(conf.conn_filter(Key('left') != '10.10.10.10')),
            ['%default', 'roadwarrior', 'myconn']
        )
        
        
        del conf['conn', 'roadwarrior']
        
        self.assertEqual(
            conf.conn_filter(
                Key('leftsubnet') == '10.1.0.0/16' or Key('right') == '%any'
            ),
            []
        )
        
if __name__ == '__main__':
    unittest.main()
