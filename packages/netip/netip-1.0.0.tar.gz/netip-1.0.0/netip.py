import urllib.request
import slower

ipv4 = urllib.request.urlopen('http://ident.me').read().decode('utf8')