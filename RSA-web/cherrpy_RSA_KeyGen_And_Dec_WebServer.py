import os
import os.path

import cherrypy
from cherrypy.lib import static
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
from pyparsing import unicode

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir) #os.getcwd : os 에 절대 경로, get cerrent working directory

class FileDemo(object):

    @cherrypy.expose
    def index(self):
        return """
        <html><body>
            <h2>Download a Key_File</h2>
            <a href = 'download'>Public Key of Web Server</a>
            </br>
            <h2>Upload a Enc_file</h2>
            <form action = "upload" method = "post" enctype = "multipart/form-data">
            filename: <input type = "file" name = "myFile" /><br/>
            <input type = "submit" />
            </form>        
        </body></html>
        """

    @cherrypy.expose
    def download(self):
        path = os.path.join(absDir, 'public_key_Bob.bin')
        return static.serve_file(path, 'application/x-download', 'attachment', os.path.basename(path))


    def RSA_Decrypt(self, upload_filename):
        received_data_base64 = open(upload_filename, "rb").read()
        recipient_private_key = RSA.import_key(open("private_key_Bob.bin").read())
        print("Web Server's Private_Key: ", recipient_private_key.export_key())
        received_data = base64.b32decode(received_data_base64)
        cipher_rsa = PKCS1_OAEP.new(recipient_private_key)
        decrypted_message = cipher_rsa.decrypt(received_data)
        print("Web Server가 수신한 메시지: ", decrypted_message.decode())
        return decrypted_message.decode()

    @cherrypy.expose
    def upload(self, myFile):

        # 전송하고자 하는 파일을 선택하는 부분
        # --> 본 파일이 위치한 폴더 위치를 지정하거나 또는 임의의 폴더를 선택하도록 설정할 수 있다.
        # upload_path = '/path/to/project/data/'
        upload_path = os.path.dirname(__file__)  # 임의의 폴더를 선택 할 수 있도록 한다.

        # 업로드된 파일을 저장하고자 하는 파일명
        # 'saved.bin'으로 저장하도록 지정함
        # 만일 업로드된 파일 이름명 그대로 저장하고자 할 경우에는 아래와 같이 설정
        # upload_filename = myFile.filename
        upload_filename = 'saved.bin'

        upload_file = os.path.normpath(os.path.join(upload_path, upload_filename)) # 유저가 저장한 파일을 그대로 불러들임
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

        decrypted_message = self.RSA_Decrypt(upload_file)

        webpage_output = """
                    <html>
                    <h1>OK. Received File...</h1>
                    <p>Let's Decrypt File Using Web Server's Private Key for RSA
                    <p>Filename: {}
                    <p>Length: {}
                    <p>Received Data: {}
                    <p>
                    <p>
                    <p>Decrypted Data: {}
                    <p>web decrypted message :{}
                    </html>
                    """.format(myFile.filename, size, myFile.content_type, html_out_text, decrypted_message)
        # 결과를 리턴 ---> 화면에 HTML 코드로 출력함
        return webpage_output


#tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')

if __name__ == '__main__':

    # ===============================================
    # BoB....

    cipher_RSA_Bob = RSA.generate(2048)
    private_key_Bob = cipher_RSA_Bob.export_key()
    file_out = open("private_key_Bob.bin", "wb")  # write binary mode
    file_out.write(private_key_Bob)
    file_out.close()

    public_key_Bob = cipher_RSA_Bob.publickey().export_key()
    file_out = open("public_key_Bob.bin", "wb")  # write binary mode
    file_out.write(public_key_Bob)
    file_out.close()

    cherrypy.quickstart(FileDemo())