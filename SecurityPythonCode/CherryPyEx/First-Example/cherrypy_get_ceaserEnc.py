import cherrypy
import string
from caesarCipherCore import encrypt, decrypt

LETTERS = string.ascii_uppercase + string.ascii_letters + string.whitespace

html_header = \
    """
    <html>
      <head>
        <title>Example of Web based Caesar Cipher</title>
      </head>
      <body>
    """

html_footer = \
    """
      <p><strong>Edited by:<a href="http://hs.ac.kr/"><em>Brother</em></a>. Powered by:<a href="http://cherrypy.org/"><em>Cherrypy</em></a> A Minimalist Python Web Framework</p>
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
                  Plaintext <input type="text" value="" name="get_plaintext" />
                  Key <input type="text" value="" name="get_key" />
                  <button type="submit">Encrypt!</button>
                </form>
                </p><p>
                <form method="post" action="post_plaintext">
                  Ciphertext <input type="text" value="" name="post_plaintext"/>
                  Key <input type="text" value="" name="post_key"/>
                  <button type="submit">Decrypt!</button>
                </form>
            """
        return html_header + html_body + html_footer

    @cherrypy.expose
    def get_cipher(self, get_plaintext, get_key):
        # cherrypy.request.method == 'GET'
        cipher = encrypt(get_plaintext, int(get_key), LETTERS)
        html_body = "<p>Ciphertext : %s !</p>" % (cipher)  # NOTE This input IS NOT SANITIZED!!!
        return html_header + html_body + html_footer

    @cherrypy.expose
    def post_plaintext(self, post_plaintext, post_key):
        # if cherrypy.request.method == 'POST':
        plaintext = decrypt(post_plaintext, int(post_key), LETTERS)
        html_body = "<p>Plaintext : %s!</p>" % plaintext  # NOTE This input IS NOT SANITIZED!!!
        return html_header + html_body + html_footer


if __name__ == '__main__':
    conf = {'/': {}
            }
    cherrypy.quickstart(GetPostMethods(), '/', conf)