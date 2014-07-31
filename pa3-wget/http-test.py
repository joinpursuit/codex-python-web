import http

from   textwrap import dedent
import unittest
from   unittest import TestCase


class TestHeader(TestCase):

    def test_parse(self):
        header = http._parse_header([
            'Header1: foo',
            'Header2: bar',
            'A-nice-header: pretty nice!',
            ])
        self.assertEqual(len(header), 3)
        self.assertEqual(header['Header1'], 'foo')
        self.assertEqual(header['Header2'], 'bar')
        self.assertEqual(header['A-nice-header'], 'pretty nice!')
        

    def test_parse_tricky(self):
        header = http._parse_header([
            'Header1: foo  ',
            'Header2:   ::bar::',
            'A-nicé-header: ¡Pretty nice!',
            ])
        self.assertEqual(len(header), 3)
        self.assertEqual(header['Header1'], 'foo')
        self.assertEqual(header['Header2'], '::bar::')
        self.assertEqual(header['A-nicé-header'], '¡Pretty nice!')
        

    def test_format_header(self):
        fields = {
            'Content-Type': 'image/jpeg',
            'Content-Length': '65536',
            'X-My-Header': 'datadatadata',
            }
        header = http._format_header(fields)
        self.assertTrue('Content-Type: image/jpeg' in header)
        self.assertTrue('Content-Length: 65536' in header)
        self.assertTrue('X-My-Header: datadatadata' in header)


    def test_parse_message(self):
        msg = b'This is the start line.\r\nHeader1: foo\r\nHeader2: bar\r\n\r\nBody.\nMore body.\nBodilicious!\n'
        start_line, header, body = http._parse_message(msg)
        self.assertEqual(start_line, 'This is the start line.')
        self.assertTrue('Header1' in header)
        self.assertEqual(header['Header1'], 'foo')
        self.assertTrue('Header2' in header)
        self.assertEqual(header['Header2'], 'bar')
        self.assertEqual(body, b'Body.\nMore body.\nBodilicious!\n')
        

    def test_format_message(self):
        msg = http._format_message(
            'My lovely start line.',
            {'X-favorite-color': 'orange',},
            b'BOOOOOOOOOOOODY')
        self.assertEqual(
            msg,
            b'My lovely start line.\r\nX-favorite-color: orange\r\n\r\nBOOOOOOOOOOOODY')


    def test_parse_request_line(self):
        method, path = http._parse_request_line('MYMETHOD /path/to/my/stuff HTTP/1.1')
        self.assertEqual(method, 'MYMETHOD')
        self.assertEqual(path, '/path/to/my/stuff')


    def test_format_request_line(self):
        line = http._format_request_line('SUZUKI', 'doremifasol')
        self.assertEqual(line, 'SUZUKI doremifasol HTTP/1.1')


    def test_parse_status_line(self):
        line = 'HTTP/1.1 666 A daemon ate your web page.'
        status, reason = http._parse_status_line(line)
        self.assertEqual(status, 666)
        self.assertEqual(reason, 'A daemon ate your web page.')


    def test_format_status_line(self):
        line = http._format_status_line(200, 'I\'m so on top of it.')
        self.assertEqual(line, 'HTTP/1.1 200 I\'m so on top of it.')


    def test_request_round_trip(self):
        req0 = http.Request(
            method  ='POST',
            path    ='/api/data',
            header  ={
                'Host': 'www.example.com',
                'Referer': 'www.searchengine.com',
                'User-Agent': 'CodeX Special Web Client',
                },
            body    ="{field: 'foo', value: 42}".encode("UTF-8"))
        # Round trip through our API.
        msg = http.format_request(req0)
        req1 = http.parse_request(msg)

        self.assertEqual(req1.method, 'POST')
        self.assertEqual(req1.path, '/api/data')
        self.assertEqual(len(req1.header), 3)
        self.assertTrue('Host' in req1.header)
        self.assertEqual(req1.header['Host'], 'www.example.com')
        self.assertTrue('Referer' in req1.header)
        self.assertEqual(req1.header['Referer'], 'www.searchengine.com')
        self.assertTrue('User-Agent' in req1.header)
        self.assertEqual(req1.header['User-Agent'], 'CodeX Special Web Client')
        self.assertEqual(req1.body, "{field: 'foo', value: 42}".encode("UTF-8"))


    def test_response_round_trip(self):
        web_page = '<html><body>This is my web page!</body></html>'

        resp0 = http.Response(
            status  =200,
            reason  ='OK',
            header  ={
                'Content-Type': 'text/html',
                'Content-Length': '46',
                },
            body=web_page.encode('UTF-8'))
        # Round trip through our API.
        msg = http.format_response(resp0)
        resp1 = http.parse_response(msg)

        self.assertEqual(resp1.status, 200)
        self.assertEqual(resp1.reason, 'OK')
        self.assertEqual(len(resp1.header), 2)
        self.assertTrue('Content-Type' in resp1.header)
        self.assertEqual(resp1.header['Content-Type'], 'text/html')
        self.assertTrue('Content-Length' in resp1.header)
        self.assertEqual(resp1.header['Content-Length'], '46')
        self.assertEqual(resp1.body, web_page.encode('UTF-8'))



if __name__ == '__main__':
    unittest.main()

