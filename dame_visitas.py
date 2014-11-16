import feedparser
import mechanize
import urllib
import socks
import socket
import time
import random
from stem import Signal
from stem.control import Controller
import sys

'''

Usa mechanize para dar accesos a un blog.
Toma como referencia el feed de atom del blog.

*Usa Tor para cambiar ip de acceso
*Usa socks para configurar el socket de salida
*Usa Stem para cambiar la id de tor cada vez que se ejecuta
*Usa feedparser para extraer urls del atom

Accede a un número aleatorio de las entradas de atom y en orden también aleatorio

https://stem.torproject.org/faq.html#how-do-i-request-a-new-identity-from-tor


'''
if len(sys.argv) == 1:
    print "Uso {} <url del feed atom>"
    sys.exit()

atom = sys.argv[1]


lista = feedparser.parse(urllib.urlopen(atom))

links = [l.link for l in lista.entries]
random.shuffle(links)

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

def nueva_id():
    # Puerto de control de Tor: 9151
    with Controller.from_port(port = 9151) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

# cambia id de Tor cada vez que se ejecuta
nueva_id()

# Configura proxy Tor: 9150
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)

# patch the socket module
socket.socket = socks.socksocket
socket.create_connection = create_connection

browser = mechanize.Browser()
print browser.open('http://icanhazip.com').read()
browser.set_handle_robots(False)
browser.set_handle_refresh(False)
browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

n = random.randint(1, len(links))
print "Voy a mirar", n, "links ..."

for l in links[:n]:
    data = browser.open(l.encode()).read()
    print l, '-->', len(data)
    time.sleep(random.randint(1,20)/10.)


