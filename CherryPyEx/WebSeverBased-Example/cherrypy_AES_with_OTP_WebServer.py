import os
import os.path
import random
import string
import cherrypy
import base64
from pyparsing import unicode
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

LETTERS = string.ascii_uppercase

seed_number = ""

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """
                <html>
                <head><title>Random Seed Generator</title></head>
                <body>
                <h1>Are You Want to Generate a Seed Number</h1>
                <form action="generate_submitPage" method="get">
                    Generate Random Number:<input type="submit" />
                </form>
                <p1> Click Button for Generate Random Seed Number
                </body>
                </html>"""

    def AES_Decrypt(self, upload_file, seed_number):
        received_data = open(upload_file, "rb").read()
        IV = received_data[:16]    # 앞 부분 16바이트..
        print("IV:", IV)
        key_AES = SHA256.new(''.join(seed_number).encode()).digest()[:16]  # Seed 값 기반으로 키 생성...
        cipher_AES = AES.new(key_AES, AES.MODE_CBC, IV)  # Web Server의 Private_Key를 읽어들임
        decrypted_msg = unpad(cipher_AES.decrypt(base64.b32decode(received_data[16:])), AES.block_size)
        return decrypted_msg.decode()

    @cherrypy.expose
    def upload_AES_File(self, myFile):
        global seed_number
        # upload_path = '/path/to/project/data/'
        upload_path = os.path.dirname(__file__)  # 임의의 폴더를 선택할 수 있도록 하는 부분

        # 업로드된 파일을 저장하고자 하는 파일명        # 'saved.bin'으로 저장하도록 지정함
        upload_filename = 'saved_AES.bin'

        upload_file = os.path.normpath(os.path.join(upload_path, upload_filename))
        size = 0

        html_out_text = ""

        with open(upload_file, 'wb') as out:
            while True:
                data = myFile.file.read(8192)
                if not data:
                    break
                out.write(data)
                html_out_text += unicode(data)
                print(data)
                size += len(data)
        out.close()

        decrypted_message = self.AES_Decrypt(upload_file, seed_number)  # RSA 복호화 과정을 수행하는 함수 호출

        webpage_output = """
                    <html>
                    <h1>OK. Received File...</h1>
                    <p>Let's Decrypt File...
                    <p>Filename: {}
                    <p>Length: {}
                    <p>Mime-type: {}
                    <p>Received Data: {}
                    <p>
                    <p>
                    <p>Decrypted Data: {}
                    </html>
                  """.format(myFile.filename, size, myFile.content_type, html_out_text, decrypted_message)
        # 결과를 리턴 --> 화면에 HTML 코드로 출력함...
        return webpage_output

    @cherrypy.expose
    def generate_submitPage(self):
        global seed_number
        seed_number = random.sample(string.hexdigits, 8)
        return """
                        <html>
                        <head><title>Random Seed Generator</title></head>
                        <body>
                        <h1>Seed Number</h1>
                        <p1>{}
                        <h2>Upload a file</h2>
                        <form action="upload_AES_File" method="post" enctype="multipart/form-data">
                            filename: <input type="file" name="myFile" /><br />
                            <input type="submit" />
                        </form>
                        <h2>Download a file</h2>
                        </body>
                        </html>""".format(''.join(seed_number))

    @cherrypy.expose
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
    #
    # 실행 순서 (및 로직)
    # 서버 : cherrypy_AES_with_OTP_WebServer.py 실행
    # 서버 : http://127.0.0.1:8080 부분 클릭해서 웹서버 실행
    # 클라이언트 : 웹 페이지에서 'Generate' 버튼을 클릭해서 Seed Number를 생성함
    # 클라이언트 : cherrypy_AES_with_OTP_Client.py 실행
    # 클라이언트 : 웹 페이지에 생성된 Seed Number를 긁어서 입력하고 엔터키 --> encrypted_data_AES_for_Upload.bin 생성됨
    # 클라이언트 : 웹 페이지에 encrypted_data_AES_for_Upload.bin 파일을 업로드함
    # 서버 : 업로드된 파일에 대해 복호화 과정을 자동으로 수행하고 복호화 결과를 화면에 표시함
    # 서버 : 클라이언트로부터 업로드된 파일을 saved_AES.bin 파일로 생성함
    cherrypy.quickstart(StringGenerator())
    cherrypy.engine.exit()