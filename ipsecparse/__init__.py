"""
Use the loads function to load the ipsec configuration from a string.
You get an IpsecConf object, which is a subclass of OrderedDict.

Each section of the configuration file is represented as a
 ('section_type', 'section_name') entry in the dictionnary.
Each section is itself an instance of OrderedDict.

Ex:

from ipsecparse import loads, dumps

conf = loads(open('/etc/ipsec.conf').read())

conf['config', 'setup']['nat_traversal'] = 'yes'
conf['conn', 'myconn']['left'] = '192.168.0.10'

conf['conn', 'mynewconn'] = OrderedDict(
    leftsubnet = '10.0.0.0/16',
    right = '192.168.0.1'
)

del conf['conn', 'myconn']

with open('/etc/ipsec.conf', 'w') as fd:
    fd.write(dumps(conf))
    
A bit more documentation is available at:
    https://github.com/leforestier/ipsecparse/blob/master/README.rst
"""
    

__author__ = "Benjamin Le Forestier (benjamin@leforestier.org)"
__version__ = '0.1.0'


from ipsecparse.parser import loads
from ipsecparse.queries import Key, Keys
from ipsecparse.structures import IpsecConf

def dumps(ipsec_conf, indent = '\t'):
    return ipsec_conf.dumps(indent = indent)
