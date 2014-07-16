#!/usr/bin/env python


import unittest
from urllib import request

import fetch


class TestFetchUrlarse(unittest.TestCase):

    def test_scheme(self):
        url = 'foo://example.com'
        a = fetch.urlparse(url).scheme
        b = request.urlparse(url).scheme
        self.assertEqual(a, b)

    def test_scheme_case(self):
        url = 'FOO://example.com'
        a = fetch.urlparse(url).scheme
        b = request.urlparse(url).scheme
        self.assertEqual(a, b)

    def test_no_scheme_but_port(self):
        url = '//example.com:8042'
        a = fetch.urlparse(url).scheme
        b = request.urlparse(url).scheme
        self.assertEqual(a, b)

    def test_no_scheme(self):
        url = '//example.com'
        a = fetch.urlparse(url).scheme
        b = request.urlparse(url).scheme
        self.assertEqual(a, b)

    def test_netloc(self):
        url = 'foo://example.com'
        a = fetch.urlparse(url).netloc
        b = request.urlparse(url).netloc
        self.assertEqual(a, b)

    def test_netloc_case(self):
        url = 'foo://EXAMPLE.com'
        a = fetch.urlparse(url).netloc
        b = request.urlparse(url).netloc
        self.assertEqual(a, b)

    def test_netloc_no_scheme(self):
        url = '//example.com'
        a = fetch.urlparse(url).netloc
        b = request.urlparse(url).netloc
        self.assertEqual(a, b)

    def test_no_netloc(self):
        url = 'www.example.com'
        a = fetch.urlparse(url).netloc
        b = request.urlparse(url).netloc
        self.assertEqual(a, b)
        a = fetch.urlparse(url).path
        b = request.urlparse(url).path
        self.assertEqual(a, b)

    def test_path(self):
        url = '//example.com:8042/over/there'
        a = fetch.urlparse(url).path
        b = request.urlparse(url).path
        self.assertEqual(a, b)

    def test_path_with_query(self):
        url = '//example.com:8042/over/there?name=ferret'
        a = fetch.urlparse(url).path
        b = request.urlparse(url).path
        self.assertEqual(a, b)
        a = fetch.urlparse(url).query
        b = request.urlparse(url).query
        self.assertEqual(a, b)
    
    def test_path_ended_with_pound(self):
        url = '//example.com:8042/over/there#name=ferret'
        a = fetch.urlparse(url).path
        b = request.urlparse(url).path
        self.assertEqual(a, b)
        a = fetch.urlparse(url).query
        b = request.urlparse(url).query
        self.assertEqual(a, b)

    def test_path_with_query_and_fragment(self):
        url = '//example.com:8042/over/there?name=ferret#nose'
        a = fetch.urlparse(url).path
        b = request.urlparse(url).path
        self.assertEqual(a, b)
        a = fetch.urlparse(url).query
        b = request.urlparse(url).query
        self.assertEqual(a, b)
        a = fetch.urlparse(url).fragment
        b = request.urlparse(url).fragment
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
