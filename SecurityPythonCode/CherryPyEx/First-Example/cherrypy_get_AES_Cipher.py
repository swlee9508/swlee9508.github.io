import cherrypy
import os
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import base64

BLOCK_SIZE = 16
KEY_SIZE=32

key = os.urandom(KEY_SIZE)
IV = Random.new().read(BLOCK_SIZE)

html_header = \
    """
    <html>
      <head>
        <title>Example of Web based AES Cipher</title>
      </head>
      <body>
    """

html_footer = \
    """
      <p><strong>Edited by:<a href="http://hs.ac.kr/"><em>Brother</em></a>. 
         Powered by:<a href="http://cherrypy.org/"><em>Cherrypy</em></a> 
         A Minimalist Python Web Framework</p>
      </body>
    </html>
    """

class GetPostMethods(object):

    @cherrypy.expose
    def index(self):
        html_body = \
            """
                <p>
                <form method="get" action="get_cipher">
                  Plaintext <input type="text" value="" name="get_plaintext"/>
                  Key <input type="text" value="" name="get_key"/>
                  <button type="submit">AES_Encrypt!</button>
                </form>
                </p><p>
                <form method="post" action="post_plaintext">
                  Ciphertext <input type="text" value="" name="post_plaintext"/>
                  Key <input type="text" value="" name="post_key"/>
                  <button type="submit">AES_Decrypt!</button>
                </form>
                </p>
            """
        return html_header + html_body + html_footer

    def AESencrypt(self, message, passphrase):
        cipher = AES.new(passphrase, AES.MODE_CFB, IV)
        return cipher.encrypt(message)

    def AESdecrypt(self, encrypted, passphrase):
        cipher = AES.new(passphrase, AES.MODE_CFB, IV)
        return cipher.decrypt(encrypted)

    @cherrypy.expose
    def get_cipher(self, get_plaintext, get_key):
        # if cherrypy.request.method == 'GET':
        key = SHA256.new(get_key.encode()).digest()
        keySlice = key[:16]
        cipher = self.AESencrypt(get_plaintext.encode(), keySlice)
        html_body = "<p>Key:%s</p>" % keySlice
        html_body += "<p>Key(base64 & decode):%s</p>" % (base64.b32encode(keySlice).decode())
        html_body += "<p>Ciphertext:%s</p>" % (base64.b32encode(cipher).decode())
        html_shutdown = "<a id='shutdown'; href='./shutdown'>Shutdown Server</a>"
        return html_header + html_body + html_shutdown + html_footer

    @cherrypy.expose
    def post_plaintext(self, post_plaintext, post_key):
        # if cherrypy.request.method == 'POST':
        key = SHA256.new(post_key.encode()).digest()
        keySlice = key[:16]
        plaintext = self.AESdecrypt(base64.b32decode(post_plaintext.encode()), keySlice)
        html_body = "<p>Key:%s</p>" % keySlice
        html_body += "<p>Key(base64 & decode):%s</p>" % (base64.b32encode(keySlice).decode())
        html_body += "<p>Plaintext:%s</p>" % str(plaintext.decode())
        html_shutdown = "<a id='shutdown'; href='./shutdown'>Shutdown Server</a>"
        return html_header + html_body + html_shutdown + html_footer

    @cherrypy.expose
    def shutdown(self):
        cherrypy.engine.exit()

if __name__ == '__main__':
    #conf = {'/': {} }
    #cherrypy.quickstart(GetPostMethods(), '/', conf)
    cherrypy.config.update({'server.socket_port': 8081})
    cherrypy.quickstart(GetPostMethods())
    #cherrypy.process.wspbus.STOPPING()