#!/usr/bin/env python


from collections import namedtuple
from urllib import request


ParseResult = namedtuple('ParseResult', 'scheme, netloc, path, params, query, fragment')


# urlparse() parses a URL into its components. Below is an example URL with its
# components listed by name:
#
#    foo://example.com:8042/over/there?name=ferret#nose
#    \_/   \______________/\_________/ \_________/ \__/
#     |           |            |            |        |
#    scheme     authority     path        query   fragment
#
# For details, see: http://tools.ietf.org/html/rfc3986
def urlparse(url):
    url = url.lower()
    scheme = netloc = path = query = fragment = ''

    # Your code here

    return ParseResult(scheme, netloc, path, '', query, fragment)


if __name__ == '__main__':
    url = 'foo://example.com:8042/over/there?name=ferret#nose'
    print(url)
    print(request.urlparse(url))
    print(urlparse(url))
