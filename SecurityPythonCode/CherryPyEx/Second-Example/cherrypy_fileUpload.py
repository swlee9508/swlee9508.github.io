import os
import cherrypy
from pyparsing import unicode
# pyparsing 모듈 설치

# config = {
#     'global': {
#         'server.socket_host': '127.0.0.1',
#         'server.socket_port': 8080
#     }
# }


class App:

    @cherrypy.expose
    def file_upload(self, ufile):
        # 전송하고자 하는 파일을 선택하는 부분
        # --> 본 파일이 위치한 폴더 위치를 지정하거나 또는 임의의 폴더를 선택하도록 설정할 수 있음
        #upload_path = '/path/to/project/data/'
        #upload_path = '/Users/brother/PycharmProjects/InventWithPython/CherryPy-By-Example-Code/Second-Example/'
        upload_path = os.path.dirname(__file__)   # 임의의 폴더를 선택할 수 있도록 하는 부분 (현재 이것이 실행되고 있는 폴더에 저장 된다.)

        # 업로드된 파일을 저장하고자 하는 파일명
        # 'saved.txt'로 저장하도록 지정
        # 만일 업로드된 파일 이름명 그대로 저장하고자 할 경우에는 아래와 같이 설정
        # upload_filename = ufile.filename
        upload_filename = 'saved.txt'

        upload_file = os.path.normpath(os.path.join(upload_path, upload_filename))
        size = 0

        html_out_text = ""

        with open(upload_file, 'wb') as out:
            while True:
                data = ufile.file.read(8192)# 8192bit 만큼을 읽어서 저장 한다.
                if not data:
                    break
                out.write(data)
                html_out_text += unicode(data)
                print(data)
                size += len(data)
        out.close()
        webpage_output = """
                <html>
                <p>File received.
                <p>Filename: {}
                <p>Length: {}
                <p>Mime-type: {}
                <p>Data: {}
                </html>
              """.format(ufile.filename, size, ufile.content_type, html_out_text)

        #.format()
        # ex)
        # name = 'lee'
        # "ffwaf {} ".format(name)
        # ffwaf lee 가 출력됨

        return webpage_output


if __name__ == '__main__':
    #cherrypy.quickstart(App(), '/', config)
    cherrypy.quickstart(App())
    # 실행 순서
    # cherrypy_fileUploader.py를 실행 (http://127.0.0.1:8080 부분을 클릭하지 않음)
    # 별도의 웹 브라우져에서 webpage.html을 실행
    # 파일 업로드 수행
    # 업로드한 파일이 saved.txt로 생성되는지 확인