from distutils.core import setup
import sys

if sys.version_info < (2 , 7):
    install_requires = ['ply>=3.4', 'ordereddict']
else:
    install_requires = ['ply>=3.4']

with open('README.rst') as fd:
    long_description = fd.read()

setup(
    name='ipsecparse',
    version='0.2.0',
    packages=['ipsecparse'],
    install_requires = install_requires,
    author = 'Benjamin Le Forestier',
    author_email = 'benjamin@leforestier.org',
    url = 'https://github.com/leforestier/ipsecparse',
    keywords = ["ipsec", "conf", "configuration", "parser", "parsing", "ipsec.conf", "openswan"],
    description = "Parse and edit your ipsec configuration files",
    long_description = long_description,
    classifiers = [
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]  
)
