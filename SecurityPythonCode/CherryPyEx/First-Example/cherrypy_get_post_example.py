import cherrypy

html_header = \
    """
    <html>
      <head>
        <title>Example of GET and POST</title>
      </head>
      <body>
    """

html_footer = \
    """
      <p><strong>Powered by:<a href="http://cherrypy.org/"><em>Cherrypy</em> A Minimalist Python Web Framework</a></p>
      </body>
    </html>
    """


class GetPostMethods(object):

    @cherrypy.expose
    def index(self):
        html_body = \
            """
                <p>
                <form method="get" action="get_hello">
                  <input type="text" value="" name="get_name" />
                  <button type="submit">GET Hello!</button>
                </form>
                </p><p>
                <form method="post" action="post_hello">
                  <input type="text" value="" name="post_name"/>
                  <button type="submit">POST Hello!</button>
                </form>
            """
        return html_header + html_body + html_footer

    @cherrypy.expose
    def get_hello(self, get_name):
        # cherrypy.request.method == 'GET'
        html_body = "<p>Hello %s!</p>" % get_name  # NOTE This input IS NOT SANITIZED!!!
        return html_header + html_body + html_footer

    @cherrypy.expose
    def post_hello(self, post_name):
        # if cherrypy.request.method == 'POST':
        html_body = "<p>Hello %s!</p>" % post_name  # NOTE This input IS NOT SANITIZED!!!
        return html_header + html_body + html_footer


if __name__ == '__main__':
    conf = {'/': {}
            }
    cherrypy.quickstart(GetPostMethods(), '/', conf)