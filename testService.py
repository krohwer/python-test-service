import logging
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs

logging.basicConfig(level=logging.DEBUG)


class BaseAppService(BaseHTTPRequestHandler):

    HTTP_STATUS_RESPONSE_CODES = {
        'OK': HTTPStatus.OK,
        'FORBIDDEN': HTTPStatus.FORBIDDEN,
        'NOT_FOUND': HTTPStatus.NOT_FOUND,
    }

    # Here's a function to extract GET parameters from a URL
    def extract_GET_parameters(self):
        path = self.path
        parsedPath = urlparse(path)
        paramsDict = parse_qs(parsedPath.query)
        logging.info('GET parameters received: ' + json.dumps(paramsDict, indent=4, sort_keys=True))
        return paramsDict

    ## GET REQUEST HANDLING ##

    def do_GET(self):
        path = self.path
        paramsDict = self.extract_GET_parameters()
        status = self.HTTP_STATUS_RESPONSE_CODES['NOT_FOUND']
        responseBody = {}

        if '/python' in path:
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']

            response = "Python service is up and running!"

            responseBody['data'] = response

        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response = json.dumps(responseBody)
        logging.info('Response: ' + response)
        byteStringResponse = response.encode('utf-8')
        self.wfile.write(byteStringResponse)


if __name__ == '__main__':
    hostName = "localhost"
    serverPort = 8082
    appServer = HTTPServer((hostName, serverPort), BaseAppService)
    logging.info('Server started http://%s:%s' % (hostName, serverPort))

    try:
        appServer.serve_forever()
    except KeyboardInterrupt:
        pass

    appServer.server_close()
    logging.info('Server stopped')
