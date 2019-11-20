import os
import os.path

import cherrypy
from cherrypy.lib import static
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
from pyparsing import unicode

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

class FileDemo(object):

    @cherrypy.expose
    def index(self):
        return """
        <html><body>
            <h2>Download a file</h2>
            <a href = 'download'>Public Key of Web Server</a>
        </body></html>
        """

    @cherrypy.expose
    def download(self):
        path = os.path.join(absDir, 'public_WebServer.bin')
        return static.serve_file(path, 'application/x-download', 'attachment', os.path.basename(path))


if __name__ == '__main__':
    # 실행순서 (및 로직)
    # 서버: cherrypy_RSA_KeyGen_And_Dec_WebServer.py 실행
    # 서버: Web Server의 Public_Key/ Private_Key 파일을 각각 생성함
    # 서버: http://127.0.0.1:8080 부분 클릭해서 웹서버 실행
    # 클라이언트: 웹 페이지에서 Public_Key 파일 다운로드 받음
    # 클라이언트: 다운받은 Public_Key를 폴더에 복사해 놓음
    # 클라이언트: cherrypy_RSA_KeyDownload_And_Enc_Client.py 실행 ---> encrypted_data_from_Alice 파일이 만들어짐
    # 클라이언트: 웹 페이지에 encrypted_data_from_Alice.bin 파일을 업로드함.
    # 서버: 업로드된 파일에 대해 복호화 과정을 자동으로 수행하고 복호화 결과를 화면에 표시함

    # Web Server(Bob)의 공개키/개인키는 한번 만 생성하면 됨..
    key = RSA.generate(2048)
    private_key = key.export_key()    #Web Server의 Private_Key
    file_out = open("private_WebServer.bin", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()       #Web Server의 Public_Key
    file_out = open("public_WebServer.bin", "wb")
    file_out.write(public_key)
    file_out.close()

    cherrypy.quickstart(FileDemo())
