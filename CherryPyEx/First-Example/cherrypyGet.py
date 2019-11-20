import cherrypy
import string
from caesarCipherCore import encrypt, decrypt

LETTERS = string.ascii_uppercase + string.ascii_letters + string.whitespace

class GetMessage(object):

    @cherrypy.expose()
    def index(self):
        html_body = \
        """
            <html>
            <body>
            <p>
            <form method ="get" action="get_msg">
                <input type="text" value="" name="input_msg" />
                <input type="text" value="" name="key" />
                <button type="submit">Click!</button>
            </form>
            </body>
            </html>
            """
        return html_body

    @cherrypy.expose()
    def get_msg(self, input_msg,key):
        return "Cipher Text %s!" % encrypt(input_msg,int(key),LETTERS)


if __name__ == '__main__':
    cherrypy.quickstart(GetMessage())