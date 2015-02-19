Parse and edit your ipsec configuration files (ipsec.conf)

Installation
~~~~~~~~~~~~

To install ipsecparse, simply:

.. code-block:: console

    pip install ipsecparse

Examples
~~~~~~~~

.. code:: python
    
    # Load the configuration from a string.
    
    from ipsecparse import loads
    
    conf = loads(open('/etc/ipsec.conf').read())
    
    # The configuration is represented as a dictionnary
    # (actually a subclass of OrderedDict)
    
    # Each section of the configuration is an OrderedDict.
    
    # Let's modify some settings:
    
    conf['config', 'setup']['nat_traversal'] = 'yes'
    
    conf['conn', 'myconn']['left'] = '192.168.0.10'
    
    # Create a connection:
    
    conf['conn', 'mynewconn'] = {
        'leftsubnet': '10.0.0.0/16',
        'right': '192.168.0.1'
    }
    
    # You can also use an OrderedDict if order matters to you:
    
    from collections import OrderedDict
    
    conf['conn', 'mynewconn'] = OrderedDict(
        lefsubnet = '10.0.0.0/16',
        right = '192.168.0.1'
    )
    
    # Delete a connection:
    
    del conf['conn', 'mynewconn']
    
    # Same thing with certification authorities. Create a CA:
    
    conf['ca', 'myca'] = {
        'cacert': 'MyCert.pem',
        'crluri': 'http://crl.example.com/mycrl.crl',
        'auto': 'add'
    }
    
    # Delete it:
    
    del conf['ca', 'myca']
    
    # Add an include:
    
    conf['include', '/etc/ipsec.d/ipsec.include'] = True
    
    # Delete it:
    
    del conf['include', '/etc/ipsec.d/ipsec.include']
    
    # Display the new configuration as a string:
    
    print(conf.dumps())
    
    # with four spaces indents instead of the default tabulations:
    
    print(conf.dumps(indent = '    '))
    
    # Replace the old configuration file:
    
    with open('/etc/ipsec.conf', 'w') as fd:
        fd.write(conf.dumps())
    
    # Search for connections inside the configuration.
    # Pass a callable to the `conn_filter` method.
    
    for name, section in conf.conn_filter(
        lambda conn: conn.get('leftsubnet') == '10.0.0.0/16'
    ):
        section['auto'] = 'start'
        
    # Or use the Key and Keys class
    # (just to make queries a bit shorter)
    
    from ipsecparse import Key, Keys
    
    for name, section in conf.conn_filter(
        Key('leftsubnet') == '10.0.0.0/16'
    ):
        section['auto'] = 'start'
    
    for name, section in conf.conn_filter(
        Keys('left', 'right').contains('192.168.0.1')
    ):
        del conf['conn', name]


GitHub repo: https://github.com/leforestier/ipsecparse

    

