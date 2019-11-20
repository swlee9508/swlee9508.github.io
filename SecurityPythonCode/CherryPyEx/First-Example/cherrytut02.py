import random
import string
from .caesarCipherCore import decrypt, encrypt

import cherrypy

LETTERS = string.ascii_uppercase

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """
                <html>
                <head><title>Hello World</title></head>
                <body>
                <h1>Hello World</h1>
                <p1> This is Sample Page
                </body>
                </html>"""

    @cherrypy.expose
    def generate(self):
        return ''.join(random.sample(string.hexdigits, 8))

    @cherrypy.expose
    def encrypt(self):
        return ''.join(encrypt('HELLO', 4, LETTERS))

    @cherrypy.expose()
    def about(self):
        return """
                <html>
                <head><title>About Us</title></head>
                <body>
                <h1>About Us</h1>
                <p1> This is our first class python using cherrypy. </p1>
                </body>
                </html>
                """

if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator())
