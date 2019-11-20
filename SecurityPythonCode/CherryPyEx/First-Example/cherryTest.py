import cherrypy
import random,string

def encrypt(message,key,LETTERS):
    encrypt_message=''
    for symbol in message:
        if symbol in LETTERS:
            num = ( LETTERS.find(symbol) + key ) % (len(LETTERS))
            encrypt = LETTERS[num]
        else:
            encrypt = symbol
        encrypt_message = encrypt_message + encrypt
    return encrypt_message

def decrypt(encrypt_message,key,LETTERS):
    decrypt_message=''
    for symbol in encrypt_message:
        if symbol in LETTERS:
            num = ( LETTERS.find(symbol) - key ) % (len(LETTERS))
            decrypt = LETTERS[num]
        else:
            decrypt = symbol
        decrypt_message = decrypt_message + decrypt
    return decrypt_message


LETTERS = string.ascii_lowercase

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        # (""") 여러줄에 걸쳐서 코딩 하겠다는 의미
        return """ 
                <html>
                <head><title>Hello World</title></head>
                <body>
                <h1>Hello World</h1>
                <p1> This is cherryPy Sample Page </p1>
                </body>
                </html>
                 <p>
                <form method="get" action="get_encrypt">
                  <input type="text" value="" name="get_name" />
                  <input type="text" value="" name="key" />
                  <button type="submit">GET encrypt!</button>
                </form>
                </p>
                 <p>
                <form method="get" action="get_decrpyt">
                  <input type="text" value="" name="get_name" />
                  <input type="text" value="" name="key" />
                  <button type="submit">GET decrypt!</button>
                </form>
                </p>
                """
    @cherrypy.expose
    def get_encrypt(self, get_name,key):
        # cherrypy.request.method == 'GET'
        html_body = "<p>Hello %s!</p>" % encrypt(get_name,int(key),LETTERS) # NOTE This input IS NOT SANITIZED!!!
        return html_body

    @cherrypy.expose
    def get_decrpyt(self, get_name,key):
        html_body = "<p>Hello %s!</p>" % decrypt(get_name, int(key), LETTERS)  # NOTE This input IS NOT SANITIZED!!!
        return html_body

    @cherrypy.expose
    def about(self):
        return """
                <html>
                <head><title>About Us</title></head>
                <body>
                <h1>About Us</h1>
                <p1> 체리 파이가 이용되는 홈페이지 </p1>
                </body>
                </html>
                """

    @cherrypy.expose #랜덤하게 값을 생성하는 방법(8비트)
    def generate(self):
        return ''.join(random.sample(string.hexdigits, 8))

#return 값은 웹 클라이언트 쪽으로 return 된다.
cherrypy.quickstart(HelloWorld()) #class 를 넣어 콜 한다.